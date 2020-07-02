from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings

class Profile(models.Model):
    남성 = '남성' 
    여성 = '여성'
    GENDER_CHOICES = [(남성, '남성'),(여성, '여성'),]
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,)

    region = models.CharField(max_length=30,) 

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Closet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(blank=True, upload_to='clothes/images/')
    color = models.CharField(max_length=20, blank=True)
    