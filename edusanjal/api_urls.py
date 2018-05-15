from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.institute import api as institute_api

router = DefaultRouter()

router.register(r'institutes', institute_api.InstituteViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls))
]
