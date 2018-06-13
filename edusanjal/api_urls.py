from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.institute import api as institute_api
from apps.program import api as program_api

# router.register(r'institutes', institute_api.InstituteViewSet)

urlpatterns = [
    url(r'^institutes/colleges/$', institute_api.CollegeList.view(), name='institute-list'),
    url(r'^institutes/(?P<slug>[\w-]+)/$', institute_api.InstituteDetail.as_view(), name='institute-detail'),
    url(r'^programs/$', program_api.ProgramList.view(), name='program-list'),

]
