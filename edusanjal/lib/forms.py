from django import forms
from django.contrib.gis.geos import Point


class PointForm(forms.ModelForm):
    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=False,
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=False,
    )

    class Meta:
        exclude = []
        widgets = {'point': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('point', None)
        if isinstance(coordinates, Point):
            self.initial['latitude'], self.initial['longitude'] = coordinates.tuple

    def clean(self):
        data = super().clean()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        point = data.get('point')
        if latitude and longitude and not point:
            data['point'] = Point(longitude, latitude)
        return data