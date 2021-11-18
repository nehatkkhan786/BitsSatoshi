from django.db import models
from django.conf import settings


# Create your models here.

class AirdropUsers(models.Model):
    email = models.EmailField()
    twitter_username = models.CharField(max_length=20)
    telegram_username = models.CharField(max_length=20)
    discord_username = models.CharField(max_length=20, blank=True, null=True)
    tweet_link = models.URLField(max_length=100)
    trx_address  = models.CharField(max_length=100)


    def __str__(self):
        return self.email


