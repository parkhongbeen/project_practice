from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # username = models.CharField('username', max_length=20)
    name = models.CharField('이름', max_length=20)
