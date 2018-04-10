from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from versatileimagefield.fields import VersatileImageField

from ..media.models import Image, Document


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


class Discipline(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)


class Level(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    order = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Council(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)


class Program(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    full_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, blank=True, null=True, on_delete=models.SET_NULL)
    board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.SET_NULL)
    recognition = models.ForeignKey(Council, blank=True, null=True, on_delete=models.SET_NULL)
    related_programs = models.ManyToManyField('self', blank=True)
    duration_years = models.PositiveSmallIntegerField(blank=True, null=True)
    duration_months = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField()
    eligibility = models.TextField(blank=True, null=True)
    job_prospects = models.TextField(blank=True, null=True)
    salient_features = models.TextField(blank=True, null=True)
    curricular_stucture = models.TextField(blank=True, null=True)
    admission_criteria = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    disciplines = models.ManyToManyField(Discipline, blank=True, related_name='programs')

    # TODO 
    # careers =
