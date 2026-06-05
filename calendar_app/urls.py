from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('calendar/', views.monthly_view, name='monthly_view'),
    path('calendar/weekly/', views.weekly_view, name='weekly_view'),
    path('dashboard/pending-leaves/', views.pending_unavailability, name='pending_unavailability'),
    path('dashboard/submit-leave/', views.submit_leave_request, name='submit_leave_request'),
]