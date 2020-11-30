from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Restaurants import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('items', views.itemViewSet)

app_name = 'Restaurants'

urlpatterns = [
    path('', include(router.urls))
]
