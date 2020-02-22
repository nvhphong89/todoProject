from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.User.username} profile'

    # Create a save method to override the parent save() method
    def save(self):
        # execute the parent save method first
        super().save()
        # then grab the saved profile pic and resize it using Pillow library
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
