from django.db import models


class List(models.Model):
    name = models.TextField(max_length=30, blank=False, null=True)


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List, blank=False, null=True)

    # Create a random list if not provided
    def save(self, *args, **kwargs):
        if not self.list:
            list_ = List.objects.create()
            list_.save()
            self.list = list_
        super(Item, self).save(*args, **kwargs)
