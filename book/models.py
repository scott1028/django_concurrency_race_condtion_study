from django.db import models

# Create your models here.
class book(models.Model):
	label = models.CharField(max_length=30)
	version = models.IntegerField(default=0)

class person(models.Model):
	name = models.CharField(max_length=100)
	version = models.IntegerField(default=0)
