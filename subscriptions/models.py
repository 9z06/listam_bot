from django.db import models

# Create your models here.


class Subscription(models.Model):
    chat_id = models.IntegerField(unique=True)
    last_ad = models.IntegerField(null=True)
