from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Profile model to store user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    banner_color = models.CharField(max_length=7, default='#1f2888')

# Create a signal to automatically create or update the profile when a user is created or updated
class SpeechCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='card_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.text}"