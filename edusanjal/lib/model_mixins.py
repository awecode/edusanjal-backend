from django.db import models


class SlugModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    
    class Meta:
        abstract=True
