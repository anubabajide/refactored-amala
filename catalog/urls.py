from django.urls import path
from django.conf.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('videos', VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
