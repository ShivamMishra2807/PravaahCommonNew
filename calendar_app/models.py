from django.db import models


class CalendarEvent(models.Model):
    EVENT_TYPES = [
        ('session', 'Session'),
        ('exam', 'Exam'),
        ('holiday', 'Holiday'),
        ('hostel', 'Hostel'),
        ('unavail', 'Unavailable'),
        ('leave', 'Leave'),
    ]

    COLOR_MAP = {
        'session': '#22c55e',
        'exam': '#2563eb',
        'holiday': '#0ea5e9',
        'hostel': '#f59e0b',
        'unavail': '#ef4444',
        'leave': '#10b981',
    }

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    related_module = models.CharField(max_length=50, blank=True)
    related_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.title} ({self.event_type})"

    def get_color(self):
        return self.COLOR_MAP.get(self.event_type, '#888888')


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    requester_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.requester_name} ({self.start_date} to {self.end_date})"


# ------------------------------------------------------------------
# FUTURE MODULE INTEGRATIONS
# ------------------------------------------------------------------
# Keep this section for external modules that will be integrated later,
# such as the trainers module or any other team-owned data source.
#
# When those models become available, add them here in a clean,
# commented placeholder format so they can be enabled later without
# disturbing the current working calendar and leave-request models.
#
# Example structure for future use:
# class TrainerUnavailability(models.Model):
#     trainer = models.ForeignKey('trainers.Trainer', on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     reason = models.TextField(blank=True)
#     is_approved = models.BooleanField(default=False)
#     submitted_at = models.DateTimeField(auto_now_add=True)
# ------------------------------------------------------------------
