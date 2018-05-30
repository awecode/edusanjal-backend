from time import sleep

from django.http import JsonResponse
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, OrderingFilterBackend, \
    DefaultOrderingFilterBackend, SearchFilterBackend
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from elasticsearch_dsl import SF
from elasticsearch_dsl.query import FunctionScore
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from apps.institute.documents import InstituteDoc
from apps.institute.serializers import InstituteDocSerializer
from edusanjal.lib.api import DetailView, DocList
from .models import Institute
# from .serializers import InstituteDetailSerializer, InstituteMinSerializer

from rest_framework.views import APIView


class InstituteDetail(APIView):
    """
        Retrieve an institute detail
    """

    def get(self, request, *args, **kwargs):
        try:
            return Response(Institute.get(kwargs.get('slug'), request))
        except Institute.DoesNotExist:
            return Response(status=400)


class InstituteList(DocList):
    document = InstituteDoc
    serializer_class = InstituteDocSerializer
    filter_backends = [
        FilteringFilterBackend,
        # OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    ordering = ('-featured', '-is_member', '-verified', '-is_community')
    filter_fields = {
        'type': 'type.raw'
    }
