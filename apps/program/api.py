from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, DefaultOrderingFilterBackend, SearchFilterBackend

from apps.program.models import Level
from .serializers import ProgramDocSerializer
from edusanjal.lib.api import DocList

from .documents import ProgramDoc


class ProgramList(DocList):
    document = ProgramDoc
    serializer_class = ProgramDocSerializer
    filter_backends = [
        FilteringFilterBackend,
        # OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    ordering = ()
    filter_fields = {
        'level': 'level.raw',
        # 'discipline': 'discipline.raw',
        # 'affiliation': 'affiliation.raw',

    }

    aggregation_order = {
        'level': Level.LIST
    }

    def transform_search(self, search):
        search.aggs.bucket('level', 'terms', field='level')
        # search.aggs.bucket('discipline', 'terms', field='discipline')

        # search.aggs.bucket('affiliation', 'terms', field='affiliation')

        # # global aggregation
        search.aggs.bucket('global', 'global') \
            .metric('level', 'terms', field='level') \
            # .metric('discipline', 'terms', field='discipline')
        return search
