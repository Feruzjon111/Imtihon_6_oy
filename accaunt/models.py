from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_image/default.png', null=True, blank=True)


    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",
        blank=True
    )


    def __str__(self):
        return self.username
