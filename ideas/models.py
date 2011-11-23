from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class UserMethods:
    def name(self):
        return self.first_name + " " + self.last_name

User.__bases__ += (UserMethods,)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fbid = models.BigIntegerField(default=0, primary_key=True)
    access_token = models.CharField(max_length=200, default='')

    def get_friends(self):
        return self.friends.all()

    def __unicode__(self):
        return "%s" % self.user

class Workout(models.Model):
    author = models.ForeignKey(User, related_name="author_workout")
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        name = self.author.name
        return "%s worked out at %s" % (name, self.created_at)

class WorkoutTotals(models.Model):
    author = models.ForeignKey(User, related_name="author_workouttotals")
    number = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s worked out %s times" % (self.author, self.number)

