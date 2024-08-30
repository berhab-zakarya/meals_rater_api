from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Meal, Rating
from api.serializers import MealSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # #authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                'token': token.key, 
                }, 
            status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @action(detail=True, methods=['post'])
    def rate_meal(self,request,pk=None):
        
        if  'stars' in request.data:
            '''
            create or update
            '''
            message = None
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print(user)
            status_code = None
            serializer = None
            try:
                message = 'Updated'
                rate = Rating.objects.get(meal=meal,user=user)
                rate.stars = stars
                rate.save()
                serializer = RatingSerializer(rate,many=False)
                status_code = status.HTTP_200_OK
            except:
                message = 'Created'
                rate = Rating.objects.create(stars=stars,user=user,meal=meal)
                rate.save()
                serializer = RatingSerializer(rate,many=False)
                status_code = status.HTTP_200_OK
            json = {
                    'message': 'Meal Rate '+message,
                    'result': serializer.data
                }
            return Response(json,status=status_code)
        else:    
            json = {
                'message' : 'stars not provided'
            }
            return Response(json,status=status.HTTP_400_BAD_REQUEST)
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def update(self,request,*args, **kwargs):
        response = {
            'message' : 'This is not not how you should create\\update',
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    def create(self,request,*args, **kwargs):
        response = {
            'message' : 'This is not not how you should create\\update',
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)