from edusanjal.lib.forms import PointForm
from .models import Institute


class InstituteForm(PointForm):
    class Meta(PointForm.Meta):
        model = Institute
