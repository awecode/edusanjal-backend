from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, DefaultOrderingFilterBackend, SearchFilterBackend
from rest_framework.response import Response

from apps.institute.documents import InstituteDoc
from apps.institute.serializers import InstituteDocSerializer
from edusanjal.lib.api import DocList
from .models import Institute

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
        'type': 'type.raw',
        'district': 'district.raw',
    }

    # # local aggregation
    # def transform_search(self, search):
    #     from elasticsearch_dsl import A
    #     a = A('terms', field='district')
    #     search.aggs.bucket('districts', a)

    # global aggregation
    def transform_search(self, search):
        search.aggs.bucket('count', 'global').metric('districts', 'terms', field='district')
        return search
