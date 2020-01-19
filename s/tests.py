from django.test import TestCase
from .models import *
# Create your tests here.
class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id =1, username='clyde')
        self.profile = Profile.objects.create(user = self.user,bio = 'king',email='clyde.bts17@gmail.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_profile(self):
        self.profile.save()
        profile = Profile.get_profile()
        self.assertTrue(len(profile) > 0)

class HoodTest(TestCase):
    def setUp(self):
        self.Kileleshwa = Location.objects.create(name='Kileleshwa')

        self.southside = Hood.objects.create(
            hood_name='southside',occupants_count =1, location=self.Kileleshwa)

    def test_instance(self):
        self.southside.save()
        self.assertTrue(isinstance(self.southside, Hood))

    def test_get_hoods(self):
        self.south.save()
        hoods = Hood.get_hoods()
        self.assertTrue(len(hoods) > 0)

class BusinessTest(TestCase):
    def setUp(self):
        self.mpesa= Business.objects.create(b_name='star',b_description='dope',b_email='xyz@test.com')

    def test_instance(self):
        self.mpesa.save()
        self.assertTrue(isinstance(self.mpesa,Business))

    def test_get_business(self):
        self.mpesa.save()
        business = Business.get_business()
        self.assertTrue(len(business) >0 )

class PostsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id = 1, username='clyde')
        self.Kilieleshwa = Location.objects.create(name='Kileleshwa')

        self.southside = Hood.objects.create(
            hood_name='southside',occupants_count =1, location=self.Kileleshwa)

        self.security= Posts.objects.create(title='noma',content='soja ka doze manze',posted_by= self.user, hood= self.southside)

    def test_instance(self):
        self.security.save()
        self.assertTrue(isinstance(self.security,Posts))

    def test_delete_posts(self):
        self.security.save()
        self.security.delete()
        self.assertTrue(len(Posts.objects.all()) == 0)
