from rest_framework import viewsets

from .models import Institute
from .serializers import InstituteSerializer


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
