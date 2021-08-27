from django.db import models


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=511)
    user_id = models.CharField(max_length=31)
    caught_pattern = models.CharField(max_length=255)