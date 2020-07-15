from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from .models import Product, Interest
from .serializers import ProductSerializer, InterestSerializer, UserSerializer

# Create custom permission
class PostOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST': # for POST method the action in DRF is create
            return True
        return False

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=['POST'], detail=True)
    def show_interest(self, request = None):
        if ('product' in request.data) and ('email' in request.data) and ('location' in request.data):
            product = Product.objects.get(id = pk)
            name = request.data['name']
            email = request.data['email']
            location = request.data['location']
            try:
                interest = Interest.objects.get(email = email, product = product.id)
                interest.name = name
                interest.location = location
                interest.save()

                serializer = InterestSerializer(interest, many=False)
                response = {'message': 'interest has been updated', 
                            'result': serializer.data}
                return Response(response, status = status.HTTP_200_OK)
            except:
                interest =  Interest.object.create(product = product, 
                                                    name = name, 
                                                    email = email, 
                                                    location = location)
                serializer = InterestSerializer(interest, many=False)
                response = {'message': 'rating created', 'result': serializer.data}
                return Response(response, status = status.HTTP_200_OK)
        else:
            response = {'message': 'Please provide a product, email and location', 'result': serializer.data}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
            

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (PostOnlyPermissions,)

    def delete(self, request, *args, **kwargs):
        response = {'message': 'Cannot delete Interest'}
        return Response(response, status = status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)