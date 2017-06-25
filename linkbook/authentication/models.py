from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile', primary_key=True)
	pic = models.URLField(default = "http://i.imgur.com/xz4vNF9.png")
	backend = models.CharField(max_length = 10, default = "linkbook")
	followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
	def __str__(self):
		return self.user.username

'''
def post_user_save(sender, instance, created, **kwargs):
	if not created:
		return
	print(kwargs)

	Profile.objects.get_or_create(user=instance)

post_save.connect(post_user_save, sender=User, weak=False)
'''