from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from .pagination import PageNumberPagination
from rest_framework import mixins, viewsets


class DetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'


class DocList(BaseDocumentViewSet):
    pagination_class = PageNumberPagination

    @classmethod
    def view(kls):
        return kls.as_view({'get': 'list'})
