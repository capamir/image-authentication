# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def uploadImage(request):
    image = request.FILES.get('image')

    return Response('Image was uploaded')
