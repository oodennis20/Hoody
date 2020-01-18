from django.db import models    
from pyuploadcare.dj.models import ImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Hood(models.Model):
    hood_photo = ImageField(blank=True,manual_crop='')
    hood_name = models.CharField(max_length=100, null=True)
    occupants_count = models.PositiveIntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @classmethod
    def get_hoods(cls):
        hoods = Hood.objects.all()

        return hoods

    class Meta:
        ordering = ['hood_name']


class Business(models.Model):
    b_photo = ImageField(blank=True,manual_crop='')
    b_name = models.CharField(max_length=100, blank=True, null=True)
    b_description = models.TextField(max_length=200, blank=True, null=True)
    b_email = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, related_name='biz', null=True)

    @classmethod
    def get_business(cls):
        business = Business.objects.all()

        return business

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    profile_photo = ImageField(blank=True,manual_crop='')
    bio= models.CharField(max_length=240, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    

    @receiver(post_save, sender=User)
    def create_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender,instance, **kwargs):
        instance.profile.save()
    
    
    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()

        return profile

class Join(models.Model):
	user_id = models.OneToOneField(User, on_delete=models.CASCADE,null=True )
	hood_id = models.ForeignKey(Hood, on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.user_id

class Posts(models.Model):
	title = models.CharField(max_length = 300)
	body = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	hood = models.ForeignKey(Hood, on_delete=models.CASCADE,null=True)

	def save_posts(self):
		self.save()

	def delete_posts(self):
		self.delete()

	def __str__(self):
		return self.title

class Comments(models.Model):
	comment = models.CharField(max_length = 600)
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	post = models.ForeignKey(Posts, on_delete=models.CASCADE,null=True)

	def save_comment(self):
		self.save()

	def delete_comment(self):
		self.delete()

	def __str__(self):
		return self.comment



