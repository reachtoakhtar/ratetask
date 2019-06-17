from django.db import models


class Region(models.Model):
    slug = models.CharField(max_length=55, primary_key=True)
    name = models.CharField(max_length=255)
    parent_slug = models.ForeignKey("self", to_field="slug", null=True, on_delete=models.PROTECT)


class Port(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    parent_slug = models.ForeignKey(Region, to_field="slug", on_delete=models.PROTECT)


class Price(models.Model):
    orig_code = models.ForeignKey(Port, to_field="code", on_delete=models.PROTECT, related_name="origin_code")
    dest_code = models.ForeignKey(Port, to_field="code", on_delete=models.PROTECT, related_name="destin_code")
    day = models.DateField(null=False)
    price = models.IntegerField(null=False)
