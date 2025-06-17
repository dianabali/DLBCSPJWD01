from django.utils import timezone # Import timezone for handling timestamps
from django.db import models # Import models for creating database tables
from django.contrib.auth.models import User # Import User model for user authentication
 
# Profile model to store user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    banner_color = models.CharField(max_length=7, default='#1f2888')

# SpeechCard model to store user speech cards
class SpeechCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='card_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.text}"