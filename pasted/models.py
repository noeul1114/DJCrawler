from django.db import models

# Create your models here.


class PastedData(models.Model):
    title = models.CharField(max_length=200)
    link = models.TextField()
    type = models.CharField(max_length=200)
    article = models.TextField()
    count = models.IntegerField(default=0)

    s_id = models.CharField(max_length=200, null=True)

    checked = models.BooleanField(default=False)

    first_pasted = models.DateTimeField()
    latest_published = models.DateTimeField(auto_now=True)