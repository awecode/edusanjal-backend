from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from versatileimagefield.fields import VersatileImageField

from ..program.models import Board, Program


class Personnel(models.Model):
    prefix = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255)
    photo = VersatileImageField(upload_to='personnels/')


class Designation(models.Model):
    name = models.CharField(max_length=255)
    is_founder = models.BooleanField(default=False)


INSTITUTE_TYPES = (
    ('Private', 'Private'),
    ('Public', 'Public'),
    ('Community', 'Community'),
)


class Award(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()


class Institute(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    short_name = models.CharField(max_length=15, blank=True, null=True)
    established = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                                   null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    logo = VersatileImageField(upload_to='institutes/')
    address = models.TextField(blank=True, null=True)
    district = models.ForeignKey(District, blank=True, null=True, on_delete=models.SET_NULL)
    phone = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True)
    email = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    boards = models.ManyToManyField(Board, blank=True)
    network_institutes = models.ManyToManyField('self', blank=True)
    description = models.TextField()
    salient_features = models.TextField(blank=True, null=True)
    admission_guidelines = models.TextField(blank=True, null=True)
    scholarship_information = models.TextField(blank=True, null=True)
    ugc_accredition = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    verified = models.BooleanField(default=True)

    has_building = models.BooleanField(default=False, verbose_name='Does the college own its building?')
    no_of_buildings = models.PositiveSmallIntegerField(blank=True, null=True)
    no_of_rooms = models.PositiveSmallIntegerField(blank=True, null=True)
    has_land = models.BooleanField(default=False, verbose_name='Does the college own its land?')
    land = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Land area in sq. ft.')
    total_staffs = models.PositiveSmallIntegerField(blank=True, null=True)
    class_capacity = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Max students per class')

    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    images = models.ManyToManyField(Image, blank=True)
    documents = models.ManyToManyField(Document, blank=True)


class InstituteAward(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                            null=True)
    description = models.TextField(blank=True, null=True)


class InstituteProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                            null=True)
    fee = models.IntegerField(blank=True, null=True)
    seats = models.PositiveSmallIntegerField(blank=True, null=True)
    time_slot = models.CharField(blank=True, null=True)


class Feature(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()


MEMBERSHIPS = (
    ('Premium', 'Premium')
)


class Membership(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    plan = models.CharField(max_length=20, choices=MEMBERSHIPS)


class InstitutePersonnel(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
