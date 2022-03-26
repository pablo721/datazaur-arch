from django.db import models



class Website(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    selector = models.CharField(max_length=128)



