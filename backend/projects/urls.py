from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('uploadkey', views.ImageAddressViewSet, basename='uploadkey')

urlpatterns = [
    path('upload/', views.uploadImage, name='dct')
] + router.urls
