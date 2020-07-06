from django.db import models
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


def closet_image_path(instance, filename):
    return f'closet/{instance.user.pk}/{filename}'


class Closet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(blank=True, upload_to=closet_image_path)
    color = models.CharField(max_length=20, blank=True)
    