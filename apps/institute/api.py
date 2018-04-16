from edusanjal.lib.api import DetailView
from .models import Institute
from .serializers import InstituteDetailSerializer


class InstituteViewSet(DetailView):
    queryset = Institute.objects.all()
    serializer_class = InstituteDetailSerializer
