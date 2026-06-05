import calendar as cal_lib
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import CalendarEvent, LeaveRequest


class CalendarItem:
    def __init__(self, title, event_type, start_datetime, end_datetime):
        self.title = title
        self.event_type = event_type
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def get_color(self):
        return CalendarEvent.COLOR_MAP.get(self.event_type, '#888888')


def _add_leave_requests(day_events, requests, key_type='day'):
    for req in requests:
        current = req.start_date
        while current <= req.end_date:
            key = current if key_type == 'date' else current.day
            day_events.setdefault(key, []).append(
                CalendarItem(
                    title='Leave',
                    event_type='leave',
                    start_datetime=datetime.combine(current, datetime.min.time()),
                    end_datetime=datetime.combine(current, datetime.max.time()),
                )
            )
            current += timedelta(days=1)


def dashboard_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    events = CalendarEvent.objects.filter(
        start_datetime__year=year,
        start_datetime__month=month,
    )

    pending_requests = LeaveRequest.objects.filter(status='pending')
    summary = {
        'sessions': events.filter(event_type='session').count(),
        'exams': events.filter(event_type='exam').count(),
        'holidays': events.filter(event_type='holiday').count(),
        'pending_leaves': pending_requests.count(),
    }

    return render(
        request,
        'calendar_app/dashboard.html',
        {
            'today': today,
            'year': year,
            'month': month,
            'month_name': cal_lib.month_name[month],
            'events': events[:6],
            'summary': summary,
            'color_map': CalendarEvent.COLOR_MAP,
        },
    )


def monthly_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    grid = cal_lib.monthcalendar(year, month)

    events = CalendarEvent.objects.filter(
        start_datetime__year=year,
        start_datetime__month=month,
    )

    day_events = {}

    for evt in events:
        d = evt.start_datetime.day
        day_events.setdefault(d, []).append(evt)

    _add_leave_requests(day_events, LeaveRequest.objects.all(), key_type='day')

    first = date(year, month, 1)
    prev = (first - timedelta(days=1)).replace(day=1)
    nxt = (first + timedelta(days=32)).replace(day=1)

    return render(
        request,
        'calendar_app/monthly.html',
        {
            'grid': grid,
            'day_events': day_events,
            'year': year,
            'month': month,
            'month_name': cal_lib.month_name[month],
            'prev': prev,
            'next': nxt,
            'today': today,
            'color_map': CalendarEvent.COLOR_MAP,
        },
    )


def pending_unavailability(request):
    requests = LeaveRequest.objects.all()
    return render(
        request,
        'calendar_app/pending_leaves.html',
        {
            'title': 'Pending Leaves',
            'requests': requests,
        },
    )


def submit_leave_request(request):
    if request.method == 'POST':
        LeaveRequest.objects.create(
            requester_name=request.POST.get('requester_name', 'Manager'),
            role=request.POST.get('role', 'Management'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason', 'Requested from dashboard'),
        )
        messages.success(request, 'Your leave request has been submitted and is now pending approval.')
        return redirect('pending_unavailability')

    return render(request, 'calendar_app/pending_leaves.html', {'title': 'Submit Leave Request'})


def weekly_view(request):
    today = date.today()
    start = today - timedelta(days=today.weekday())

    if request.GET.get('start'):
        start = date.fromisoformat(request.GET['start'])

    week_days = [start + timedelta(days=i) for i in range(7)]

    events = CalendarEvent.objects.filter(
        start_datetime__date__gte=week_days[0],
        start_datetime__date__lte=week_days[-1],
    ).order_by('start_datetime')

    day_events = {}

    for evt in events:
        d = evt.start_datetime.date()
        day_events.setdefault(d, []).append(evt)

    _add_leave_requests(
        day_events,
        LeaveRequest.objects.all(),
        key_type='date',
    )

    return render(
        request,
        'calendar_app/weekly.html',
        {
            'week_days': week_days,
            'day_events': day_events,
            'prev_start': (start - timedelta(days=7)).isoformat(),
            'next_start': (start + timedelta(days=7)).isoformat(),
            'today': today,
            'color_map': CalendarEvent.COLOR_MAP,
        },
    )

