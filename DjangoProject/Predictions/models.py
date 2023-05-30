from django.db import models

class File(models.Model):
    title = models.CharField(max_length= 40)
    file = models.FileField(upload_to='in')

