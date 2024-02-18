from django.urls import path
from . import views


urlpatterns = [
    path('process-image-dct', views.uploadImage, name='dct')
]
