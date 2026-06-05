"""
Utility functions for Calendar App

Trainer-related utilities are temporarily disabled
until the Trainers module is integrated.
"""

# =====================================================

# TEMPORARILY DISABLED

# Depends on TrainerUnavailability model

# Re-enable after Trainers module is integrated

# =====================================================

# import datetime

# from .models import TrainerUnavailability

#

# def check_trainer_conflict(trainer_id, date):

# if isinstance(date, datetime.datetime):

# date = date.date()

#

# return TrainerUnavailability.objects.filter(

# trainer_id=trainer_id,

# is_approved=True,

# start_date__lte=date,

# end_date__gte=date,

# ).exists()

#

#

# def get_conflicts_in_range(trainer_id, start_date, end_date):

# if isinstance(start_date, datetime.datetime):

# start_date = start_date.date()

# if isinstance(end_date, datetime.datetime):

# end_date = end_date.date()

#

# return TrainerUnavailability.objects.filter(

# trainer_id=trainer_id,

# is_approved=True,

# start_date__lte=end_date,

# end_date__gte=start_date,

# )

#
