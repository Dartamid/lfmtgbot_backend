from django.db import models


class BotUser(models.Model):
    tg_id = models.CharField(max_length=200, primary_key=True)
    access_token = models.CharField(max_length=300)
