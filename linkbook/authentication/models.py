from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username
