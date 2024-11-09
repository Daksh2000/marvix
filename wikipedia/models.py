from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    snippet = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
