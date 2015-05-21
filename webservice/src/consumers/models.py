from django.contrib.auth.models import User
from django.db import models


class Consumer(models.Model):
    user = models.OneToOneField(User, null=True)
    email = models.EmailField(unique=True)
    email_validation_code = models.CharField(max_length=6, blank=True, default='')
    phone = models.CharField(max_length=10, blank=True, default='')
    phone_validation_code = models.CharField(max_length=6, blank=True, default='')
    is_valid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
