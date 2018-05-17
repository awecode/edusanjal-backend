from rest_framework.mixins import ListModelMixin

from edusanjal.lib.api import DetailView
from .models import Institute
from .serializers import InstituteDetailSerializer, InstituteMinSerializer


class InstituteViewSet(ListModelMixin, DetailView):
    queryset = Institute.objects.all()

    def get_serializer_class(self):
        return InstituteMinSerializer if self.action == 'list' else InstituteDetailSerializer
