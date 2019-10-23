from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group

class Location(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name':'Managers'}, null=True)
    
    def __str__(self):
        return self.name
    
    def guards(self):
        return Guard.objects.filter(location=self)

#Assign Gurads from the Admin Panel
class Guard(models.Model):
    #add to guard group
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guard')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    guard_group = Group.objects.get(name='Guards')
    guard_group.user_set.add()

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} \'s Profile'

class Client(models.Model):
    pass

#Disallow self-refferential Foreign Key (managers)