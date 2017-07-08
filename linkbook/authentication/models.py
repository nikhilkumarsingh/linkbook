from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from linkbook.links.models import Link


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile', primary_key=True)
	pic = models.URLField(default = "http://i.imgur.com/xz4vNF9.png")
	backend = models.CharField(max_length = 20, default = "linkbook")
	followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank = True, null = True)
	upvoted_links = models.ManyToManyField(Link, blank = True, null = True)
	def __str__(self):
		return self.user.username