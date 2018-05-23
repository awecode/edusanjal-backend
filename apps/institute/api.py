from django.http import JsonResponse
from elasticsearch_dsl import SF
from elasticsearch_dsl.query import FunctionScore
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from apps.institute.documents import InstituteDoc
from edusanjal.lib.api import DetailView
from .models import Institute
# from .serializers import InstituteDetailSerializer, InstituteMinSerializer

from rest_framework.views import APIView


@api_view(['GET'])
def institute_detail(request, slug, format=None):
    """
    Retrieve an institute detail
    """

    try:
        return Response(Institute.get(slug))
    except Institute.DoesNotExist:
        return Response(status=400)

        # class InstituteViewSet(ListModelMixin, DetailView):
        #     queryset = Institute.objects.all()
        # 
        #     def get_serializer_class(self):
        #         return InstituteMinSerializer if self.action == 'list' else InstituteDetailSerializer
        # 
        #     def list(self, request, *args, **kwargs):
        #         res = InstituteDoc.search()
        # location_point= {
        #     'origin': {
        #         'lat': 27,
        #         'lon': 85
        #     },
        #     'offset': '1km',
        #     'scale': '1km',
        #     'decay': '0.1'
        # }
        # res.query = FunctionScore(query=res.query, functions=[SF('gauss', coordinate=location_point)])
        # for hit in res:
        #     print(hit.name)
        #     print(hit.coordinate)
        #     print(hit.meta.score)
        # return JsonResponse({})
