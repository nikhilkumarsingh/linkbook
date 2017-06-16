from django.contrib.auth.models import User
from django.db import models


class Activity(models.Model):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
        )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length = 1, choices = ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add = True)
    link = models.IntegerField(null = True, blank = True)

    class Meta:
        verbose_name = 'Activity'

    def __str__(self):
        return self.activity_type
