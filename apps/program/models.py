from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from versatileimagefield.fields import VersatileImageField


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()


class Board(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    short_name = models.CharField(max_length=15, blank=True, null=True)
    established = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                                   null=True)
    address = models.TextField(blank=True, null=True)
    logo = VersatileImageField(upload_to='boards/')
    phone = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True)
    email = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    faculties = models.ManyToManyField(Faculty, blank=True)
    description = models.TextField()
    salient_features = models.TextField(blank=True, null=True)
    international = models.BooleanField(default=False)
    images = models.ManyToManyField(Image, blank=True)
    documents = models.ManyToManyField(Document, blank=True)


class Program(models.Model):
    pass