from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    department = models.CharField(default=None, max_length=100)
    phone = models.CharField(default=None, max_length=20)

    def __str__(self):
        return f'{self.user.username} Profile'

class Address(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=100, default=None)
    add_one = models.CharField(default=None, max_length=100)
    add_two = models.CharField(default=None, max_length=100)
    city = models.CharField(default=None, max_length=50)
    state = models.CharField(default=None, max_length=50)
    postcode = models.IntegerField(default=None)


    def __str__(self):
        return f'{self.city}, {self.country}'
