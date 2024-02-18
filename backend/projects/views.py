# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Gallery

# Create your views here.
@api_view(['POST'])
def uploadImage(request):
    image_file = request.FILES.get('image')
    image = Gallery.objects.create(image=image_file)
    return Response('Image was uploaded')
