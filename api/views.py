from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Meal, Rating
from api.serializers import MealSerializer, RatingSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    @action(detail=True, methods=['post'])
    def rate_meal(self,request,pk=None):
        if  'stars' in request.data:
            '''
            create or update
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                rate  = Rating.objects.get(meal=meal,user=user.id)
                pass
            except:
                pass
            
        else:    
            json = {
                'message' : 'stars not provided'
            }
            return Response(json,status=status.HTTP_400_BAD_REQUEST)
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    