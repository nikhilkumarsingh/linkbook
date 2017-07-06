from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from .PyOpenGraph import PyOpenGraph


from jsonfield import JSONField
from vote.models import VoteModel

class Book(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add = True)
	last_updated = models.DateTimeField(blank = True, null = True)
	title = models.CharField(max_length = 30)
	description = models.TextField(max_length = 255, default = None)
	tags = JSONField(blank=True, null=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('last_updated',)

	def save(self, *args, **kwargs):
		if not self.pk:
			super(Book, self).save(*args, **kwargs)
		else:
			self.last_updated = datetime.now()
			super(Book, self).save(*args, **kwargs)




class Link(VoteModel, models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add = True)
	url = models.URLField(default = None)
	title = models.TextField(max_length = 30)
	description = models.TextField(max_length = 1000)
	tags = TaggableManager(blank = True)
	books = models.ManyToManyField(Book)
	last_updated = models.DateTimeField(blank = True, null = True)
	og_data = JSONField(blank=True, null=True)


	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return self.title

	def save_og(self):
		self.og_data = PyOpenGraph(self.url).properties

	def save(self, *args, **kwargs):
		if not self.pk:
			self.og_data = PyOpenGraph(self.url).properties
			super(Link, self).save(*args, **kwargs)
		else:
			self.last_updated = datetime.now()
			for book in self.books.all():
				if book.tags is None:
					book.tags = {}
				for tag in self.tags.all():
					if tag.name in book.tags:
						book.tags[tag.name] += 1
					else:
						book.tags[tag.name] = 1
				book.save()
			super(Link, self).save(*args, **kwargs)



class Comment(models.Model):
    link = models.ForeignKey(Link)
    user = models.ForeignKey(User)
    text = models.TextField(max_length = 250)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.text
