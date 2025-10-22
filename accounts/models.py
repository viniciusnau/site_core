from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=255, default="")
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField("Bio", blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name or self.user.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name() or self.name
