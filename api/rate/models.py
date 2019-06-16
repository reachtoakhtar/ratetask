from django.db import models


class Port(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    parent_slug = models.CharField(max_length=255)

    class Meta:
        db_table = "ports"


class Price(models.Model):
    orig_code = models.CharField(max_length=55)
    dest_code = models.CharField(max_length=55)
    day = models.DateField()
    price = models.IntegerField()

    class Meta:
        db_table = "prices"


class Region(models.Model):
    slug = models.CharField(max_length=55)
    name = models.CharField(max_length=255)
    parent_slug = models.CharField(max_length=55)

    class Meta:
        db_table = "regions"
