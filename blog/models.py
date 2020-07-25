from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from patient.models import *



class Post(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    poster = models.ImageField(upload_to='Blog', blank=True, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, default="", on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    review = models.FloatField(default=1)
    content= models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    