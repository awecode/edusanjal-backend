from rest_framework.mixins import ListModelMixin

from edusanjal.lib.api import DetailView
from .models import Institute
from .serializers import InstituteDetailSerializer


class InstituteViewSet(ListModelMixin, DetailView):
    queryset = Institute.objects.all()
    serializer_class = InstituteDetailSerializer
