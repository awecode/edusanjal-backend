from rest_framework import mixins, viewsets


class DetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'
