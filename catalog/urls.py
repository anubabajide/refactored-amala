from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import ProductViewSet, InterestViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('interest', InterestViewSet)
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
