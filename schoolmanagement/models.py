from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    country = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    vat = models.CharField(max_length=11, null=True, blank=True)

    @property
    def full_address(self):
        return f"{self.street}, {self.zip_code}, {self.city} ({self.province})"

    def __str__(self):
        return self.name
