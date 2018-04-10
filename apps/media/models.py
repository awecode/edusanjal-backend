from django.db import models
from versatileimagefield.fields import VersatileImageField


class Image(models.Model):
    name = models.CharField(max_length=255)
    file = VersatileImageField(upload_to='images/')


class Document(models.Model):
    name = models.CharField(max_length=255)
    file = VersatileImageField(upload_to='documents/')
