from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Product, Interest, UserDetail
from .serializers import ProductSerializer, InterestSerializer, UserSerializer, UserDetailSerializer

# Custom token class
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

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
            response = {'message': 'Please provide a product, email and location'}
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (PostOnlyPermissions,)

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (PostOnlyPermissions,)

    def create(self, request=None):
        if ('username' in request.data) and ('password' in request.data) and ('location' in request.data) and ('first_name' in request.data) and ('last_name' in request.data):
            username = request.data['username']
            password = request.data['password']
            location = request.data['location']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            try:
                user = User.objects.create_user(username, 
                                            email=username, 
                                            password=password, 
                                            first_name = first_name,
                                            last_name = last_name)
                serializer1 = UserSerializer(user, many=False)
                user_detail = UserDetail.objects.create(user=user, location=location)
                serializer2 = UserDetailSerializer(user_detail, many=False)
                response = {'message': 'rating created', 'result': serializer1.data, 'location': serializer2.data}
                return Response(response, status = status.HTTP_200_OK)
            except:
                response = {'message': 'User Exists'}
                return Response(response, status = status.HTTP_400_BAD_REQUEST)
        else:
            response = {'message': 'Please provide all fields'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)