from django.contrib import admin

from .models import CalendarEvent, LeaveRequest


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'event_type',
        'start_datetime',
        'end_datetime',
        'all_day',
    )
    list_filter = ('event_type',)
    search_fields = ('title',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('requester_name', 'role', 'start_date', 'end_date', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('requester_name', 'role', 'reason')

# =====================================================

# TEMPORARILY DISABLED

# Depends on TrainerUnavailability model

# Re-enable after Trainers module is integrated

# =====================================================

#

# from .models import TrainerUnavailability

#

# @admin.register(TrainerUnavailability)

# class TrainerUnavailabilityAdmin(admin.ModelAdmin):

# list_display = (

# 'trainer',

# 'start_date',

# 'end_date',

# 'is_approved',

# 'submitted_at'

# )

# list_filter = ('is_approved',)

# actions = ['approve_selected']

#

# def approve_selected(self, request, queryset):

# queryset.update(is_approved=True)

#

# approve_selected.short_description = (

# "Approve selected unavailability requests"

# )

#
