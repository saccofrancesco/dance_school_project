from django.db import models


class School(models.Model):
    name = models.CharField(max_length=150)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip = models.CharField(max_length=20, verbose_name="CAP")
    country = models.CharField(max_length=100)
    website = models.URLField()
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    vat = models.CharField(max_length=20, verbose_name="partita IVA")
