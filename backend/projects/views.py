# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Gallery

# Create your views here.
@api_view(['POST'])
def uploadImage(request):
    try:
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the image to your Gallery model
        image = Gallery.objects.create(image=image_file)

        # Return a success response with the image URL
        return Response({'message': 'Image uploaded successfully', 'image_url': image.image.url})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
