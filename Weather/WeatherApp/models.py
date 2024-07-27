from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SearchHistory(models.Model):
    user = models.ForeignKey