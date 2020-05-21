from django.db import models


# Create your models here.
class home(models.Model):
    name = models.TextField('test', blank=True)
