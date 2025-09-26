from django.db import models

# Create your models here.
class demo_model(models.Model):
    num = models.IntegerField()
    destination = models.TextField(max_length=250)
    create_at = models.TimeField(auto_now_add=True)
    update_at = models.TimeField(auto_now=True)