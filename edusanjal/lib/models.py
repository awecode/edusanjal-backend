from django.contrib.gis.db.models import PointField
from django.db import models


class PointModel(models.Model):
    point = PointField(geography=True, srid=4326, blank=True, null=True)

    @property
    def latitude(self):
        return self.point.y

    @property
    def longitude(self):
        return self.point.x

    class Meta:
        abstract = True
