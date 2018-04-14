from rest_framework import viewsets, mixins

from .models import Institute
from .serializers import InstituteDetailSerializer


class InstituteViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteDetailSerializer
