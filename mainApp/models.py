from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# User Profile Model
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=150, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')


    def __str__(self):
        return self.user.first_name

