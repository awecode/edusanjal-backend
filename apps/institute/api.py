from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, DefaultOrderingFilterBackend, SearchFilterBackend
from rest_framework.response import Response

from apps.institute.documents import InstituteDoc
from apps.institute.serializers import InstituteDocSerializer
from apps.program.models import Level
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
    ordering = ('-featured', 'membership', '-verified', '-is_community')
    filter_fields = {
        'type': 'type.raw',
        'district': 'district.raw',
        'affiliation': 'affiliation.raw',
        'level': 'level.raw',
    }

    aggregation_order = {
        'level': Level.LIST
    }

    def transform_search(self, search):
        search.aggs.bucket('district', 'terms', field='district')
        search.aggs.bucket('type', 'terms', field='type')
        search.aggs.bucket('affiliation', 'terms', field='affiliation')
        search.aggs.bucket('level', 'terms', field='level')
        # global aggregation
        search.aggs.bucket('global', 'global') \
            .metric('district', 'terms', field='district') \
            .metric('type', 'terms', field='type') \
            .metric('affiliation', 'terms', field='affiliation') \
            .metric('level', 'terms', field='level')

        return search


class CollegeList(InstituteList):
    aggregation_skip = {
        'level': ['Pre-school', 'Primary School', 'Secondary School']
    }
