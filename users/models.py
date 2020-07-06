from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            img.thumbnail(size=(300, 300))
            img.save(self.image.path)   # override original image
