from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Interest
from .serializers import ProductSerializer, InterestSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = (AllowAny,)

    def delete(self, request, *args, *kwargs):
        response = {'message': 'Cannot delete Interest'}
        return Response(response, status = status.HTTP_400_BAD_REQUEST)