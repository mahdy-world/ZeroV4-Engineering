from django.db import models
from django.contrib.auth.models import AbstractUser
from Core.models import Modules

# Create your models here.
class User(AbstractUser):
    avater = models.ImageField(null=True, blank=True)
