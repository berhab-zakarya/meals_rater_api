from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Meal, Rating
from api.serializers import MealSerializer, RatingSerializer
from django.contrib.auth.models import User
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    @action(detail=True, methods=['post'])
    def rate_meal(self,request,pk=None):
        if  'stars' in request.data:
            '''
            create or update
            '''
            message = None
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            username = request.data['username']
            user = User.objects.get(username=username)
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
    