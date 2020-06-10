from django.db import models

# Create your models here.


class Blogs(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    img = models.ImageField(upload_to='images', default="blog-image.jpg")
    description = models.CharField(max_length=5000)
    date = models.DateField()
    creator = models.CharField(max_length=100)
