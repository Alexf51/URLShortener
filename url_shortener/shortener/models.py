from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class URL(models.Model):
    original_url = models.TextField()
    short_url = models.CharField(max_length=20, unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.original_url} -> {self.short_url}"