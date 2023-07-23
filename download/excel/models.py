from django.db import models

# Create your models here.


class Books(models.Model):
    name = models.CharField(max_length=200)
    descrp = models.CharField(max_length=500)
    pages = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Books'

