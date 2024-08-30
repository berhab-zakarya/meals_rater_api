from django.urls import include, path
from rest_framework import routers

from api.views import MealViewSet,RatingViewSet,UserViewSet

router = routers.DefaultRouter()
router.register('meals',MealViewSet)
router.register('ratings',RatingViewSet)
router.register('users',UserViewSet)
urlpatterns = [
    path('',include(router.urls)),
]
