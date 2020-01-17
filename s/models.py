from django.db import models
from django.db import models
from pyuploadcare.dj.models import ImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Location(models.Model):
    name = models.Charfield(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Hood(models.Model):
    hood_photo = ImageField(blank=True,manual_crop='')
    hood_name = models.CharField(max_length=100, blank=True, null=True)
    occupants_count = models.IntegerField(blank=True, null=True)
    location = models.ForeignKey(Location)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def get_hoods(cls):
        hoods = Hood.objects.all()

        return hoods

class Business(models.Model):
    b_photo = ImageField(blank=True,manual_crop='')
    b_name = models.CharField(max_length=100, blank=True, null=True)
    b_description = models.TextField(max_length=200, blank=True, null=True)
    b_email = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, null=True)

    @classmethod
    def get_business(cls):
        business = Business.objects.all()

        return business

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    profile_photo = ImageField(blank=True,manual_crop='')
    bio= models.CharField(max_length=240, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    u_hood = models.ForeignKey(Hood, on_delete=models.CASCADE, null=True)

    @receiver(post_save, sender=User)
    def create_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender,instance, **kwargs):
        instance.profile.save()
    
    def save_profile(self):
        self.save()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()

        return profile


