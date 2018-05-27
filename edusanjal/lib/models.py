import datetime
from django.contrib.gis.db.models import PointField
from django.db import models


class PointModel(models.Model):
    point = PointField(geography=True, srid=4326, blank=True, null=True)

    @property
    def latitude(self):
        return self.point.y if self.point else None

    @property
    def longitude(self):
        return self.point.x if self.point else None

    @property
    def coordinate(self):
        return {'lat': self.point.y, 'lon': self.point.x} if self.point else None

    class Meta:
        abstract = True


class StartEndModel(models.Model):
    start = models.DateField()
    end = models.DateField()

    @property
    def active(self):
        if self.start and self.end:
            return self.start <= datetime.date.today() <= self.end

    class Meta:
        abstract = True
