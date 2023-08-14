from django.db import models
from django.contrib.auth.models import User, AbstractUser, UserManager

# Your signal handler function
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class CustomUser(AbstractUser):
    # Add your custom fields here

    objects = UserManager()

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/')



@receiver(post_save, sender=CustomUser)
def create_user_profile_on_user_creation(sender, instance, created, **kwargs):
    print(instance,'....instance')
    if created:
        UserProfile.objects.create(user=instance)

# Connect the signal with the arguments
post_save.connect(create_user_profile_on_user_creation, sender=CustomUser)

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followed_users', on_delete=models.CASCADE)