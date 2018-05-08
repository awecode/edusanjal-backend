from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from versatileimagefield.fields import VersatileImageField

from edusanjal.lib.slug import SlugModel


class Faculty(SlugModel):
    previous_db_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Faculties'


class Board(SlugModel):
    previous_db_id = models.IntegerField(blank=True, null=True)
    short_name = models.CharField(max_length=15, blank=True, null=True)
    established = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                                   null=True)
    address = models.TextField(blank=True, null=True)
    logo = VersatileImageField(upload_to='boards/', blank=True, null=True)
    phone = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True)
    email = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    faculties = models.ManyToManyField(Faculty, blank=True)
    description = models.TextField()
    salient_features = models.TextField(blank=True, null=True)
    international = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BoardImage(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255, blank=True, null=True)
    file = VersatileImageField(upload_to='board_images/')

    def __str__(self):
        return self.name


class BoardDocument(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='board_documents/')

    def __str__(self):
        return self.name + ' - ' + self.board.name


class Discipline(SlugModel):
    previous_db_id = models.IntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Level:
    LEVELS = (
        (0, 'Pre-school'),
        (1, 'Primary School'),
        (2, 'Secondary School'),
        (3, 'Bachelors'),
        (4, 'Masters'),
    )

    LEVELS_PAIR = [(level[1], level[1]) for level in LEVELS]


class Council(SlugModel):
    previous_db_id = models.IntegerField(blank=True, null=True)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = VersatileImageField(upload_to='councils/', blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class CouncilImage(models.Model):
    council = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='council_images/')

    def __str__(self):
        return self.name


class CouncilDocument(models.Model):
    council = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = VersatileImageField(upload_to='council_documents/')

    def __str__(self):
        return self.name + ' - ' + self.council.name


class Program(SlugModel):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=30, choices=Level.LEVELS_PAIR)
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
