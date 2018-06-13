from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .pagination import PageNumberPagination


class DetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'


class DocList(BaseDocumentViewSet):
    pagination_class = PageNumberPagination
    aggregation_order = {}
    aggregation_skip = {}

    def get_aggregation_order(self):
        return self.aggregation_order

    def get_aggregation_skip(self):
        return self.aggregation_skip

    def transform_search(self, search):
        return search

    def get_queryset(self):
        return self.transform_search(self.search).query()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        qs = list(queryset)
        page = self.paginate_queryset(qs)
        aggregations = queryset._response.aggregations.to_dict()
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.paginator.get_paginated_response(serializer.data, aggregations, self.get_aggregation_order(),
                                                                   self.get_aggregation_skip())
            return paginated_data
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @classmethod
    def view(kls):
        return kls.as_view({'get': 'list'})
