from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    ip = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Topic(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Misconception(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    list_position = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TelegramMessage(models.Model):
    content = models.CharField(max_length=200)
    id = models.CharField(
        max_length=20,
        primary_key=True,
    )  # meant to contain a hash of the message content
    created_at = models.DateTimeField(auto_now_add=True)


class MessageMisconception(models.Model):
    message = models.ForeignKey(
        TelegramMessage,
        related_name="labels",
        on_delete=models.CASCADE,
    )
    misconception = models.ForeignKey(
        Misconception, related_name="instances", on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
