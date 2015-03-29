from django.db import models


class List(models.Model):
    name = models.TextField(max_length=30, blank=False, null=True)


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List, blank=False, null=True)
