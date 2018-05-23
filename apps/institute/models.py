from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from froala_editor.fields import FroalaField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.utils import build_versatileimagefield_url_set

from edusanjal.lib.image import create_set
from edusanjal.lib.models import PointModel
from edusanjal.lib.slug import SlugModel
from .nepal import DISTRICT_PAIRS
from ..program.models import Board, Program


class Personnel(models.Model):
    prefix = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255)
    photo = VersatileImageField(upload_to='personnels/')

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=255)
    is_founder = models.BooleanField(default=False)

    def __str__(self):
        return self.name


INSTITUTE_TYPES = (
    ('Private', 'Private'),
    ('Public', 'Public'),
    ('Community', 'Community'),
)


class Award(SlugModel):
    description = FroalaField()
    image = VersatileImageField(blank=True, null=True, upload_to='awards/')


class Institute(PointModel, SlugModel):
    short_name = models.CharField(max_length=15, blank=True, null=True)
    established = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                                   null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    logo = VersatileImageField(upload_to='institutes/', blank=True, null=True)
    cover_image = VersatileImageField(blank=True, null=True, upload_to='institute_covers/')
    address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=50, choices=DISTRICT_PAIRS, blank=True, null=True)
    phone = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True)
    email = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    boards = models.ManyToManyField(Board, blank=True)
    network_institutes = models.ManyToManyField('self', blank=True)

    description = FroalaField()
    salient_features = FroalaField(blank=True, null=True)
    admission_guidelines = FroalaField(blank=True, null=True)
    scholarship_information = FroalaField(blank=True, null=True)

    ugc_accredition = models.BooleanField(default=False, verbose_name='UGC Accredition')
    published = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=INSTITUTE_TYPES, default='Private')

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

    programs = models.ManyToManyField(Program, through='InstituteProgram', related_name='institutes')
    awards = models.ManyToManyField(Award, through='InstituteAward', related_name='institutes')
    personnels = models.ManyToManyField(Personnel, through='InstitutePersonnel', related_name='institutes')
    
    @classmethod
    def get(cls, slug):
        from .serializers import InstituteDetailSerializer
        return InstituteDetailSerializer(cls.objects.get(slug=slug)).data

    def __str__(self):
        return self.name

    @property
    def sizes(self):
        ret = [
            ('full', 'url'),
            ('small', 'crop__{}x{}'.format(100, 100))
        ]
        return ret

    @property
    def logo_set(self):
        return create_set(self.logo, self.sizes)

    @property
    def recent_awards(self):
        return self.awards.order_by('-id')[:3]

    @property
    def levels(self):
        return set([program.level for program in self.programs.all()])

    @property
    def awards_count(self):
        return self.awards.count()


class InstituteImage(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255)
    file = VersatileImageField(upload_to='institute_images/',
                               width_field='width',
                               height_field='height'
                               )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )

    @property
    def thumb_height(self):
        return int(self.height * 300 / self.width)

    @property
    def sizes(self):
        ret = [
            ('full', 'url'),
            ('small', 'thumbnail__{}x{}'.format(300, self.thumb_height))
        ]
        return ret

    def __str__(self):
        return self.name


class InstituteDocument(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='institute_documents/')

    def __str__(self):
        return self.name


class InstituteAward(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                            null=True)
    description = FroalaField(blank=True, null=True)
    image = VersatileImageField(blank=True, null=True, upload_to='institute_awards/')


class InstituteProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='institute_programs')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institute_programs')
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1700), MaxValueValidator(2050)], blank=True,
                                            null=True)
    fee = models.IntegerField(blank=True, null=True)
    seats = models.PositiveSmallIntegerField(blank=True, null=True)
    time_slot = models.CharField(max_length=255, blank=True, null=True)


class Feature(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()


MEMBERSHIPS = (
    ('Premium', 'Premium'),
)


class Membership(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    plan = models.CharField(max_length=20, choices=MEMBERSHIPS)


class InstitutePersonnel(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institute_personnels')
    message = FroalaField(blank=True, null=True)


class Admission(SlugModel):
    programs = models.ManyToManyField(Program, blank=True, related_name='admissions')
    institutes = models.ManyToManyField(Institute, blank=True, related_name='admissions')
    description = FroalaField()
    starts_on = models.DateField(blank=True, null=True)
    ends_on = models.DateField(blank=True, null=True)
    entrance_exam_date = models.DateField(blank=True, null=True)


class ScholarshipCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()


class Scholarship(SlugModel):
    starts_on = models.DateField(blank=True, null=True)
    ends_on = models.DateField(blank=True, null=True)
    categories = models.ManyToManyField(ScholarshipCategory)
    institutes = models.ManyToManyField(Institute, blank=True)


class Ranking(SlugModel):
    description = FroalaField()


class Rank(models.Model):
    rank = models.ForeignKey(Ranking, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(default=1)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=255, blank=True, null=True)
