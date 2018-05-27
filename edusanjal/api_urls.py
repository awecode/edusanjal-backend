from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.institute import api as institute_api
from apps.institute.api import InstituteList

router = DefaultRouter()

# router.register(r'institutes', institute_api.InstituteViewSet)

urlpatterns = [
    url(r'^institutes/(?P<slug>[\w-]+)/$', institute_api.institute_detail, name='institute-detail'),
    url(r'^institutes/$', InstituteList.view(), name='institute-list'),

]
