from django.db import models

# Create your models here.
class Gallery(models.Model):
    image = models.ImageField(null=True, blank=True)


class ImageAddress(models.Model):
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=100)
    