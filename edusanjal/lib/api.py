from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets


class DetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'


class DocList(BaseDocumentViewSet):
    @classmethod
    def view(kls):
        return kls.as_view({'get': 'list'})
