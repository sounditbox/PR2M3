from django.db import models


# ORM
class Profile(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.IntegerField()

