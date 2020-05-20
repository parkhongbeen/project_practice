from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('이름', max_length=50, unique=True)
    password = models.CharField('비밀번호', max_length=50)
    useremail = models.EmailField('이메일', max_length=50)

    def __str__(self):
        return self.username
