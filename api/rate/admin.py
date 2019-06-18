from django.contrib import admin

from rate.models import Region, Port, Price

__author__ = "akhtar"


class AdminMixin(admin.ModelAdmin):
    list_per_page = 500


class RegionAdmin(AdminMixin):
    list_display = [f.name for f in Region._meta.fields]


class PortAdmin(AdminMixin):
    list_display = [f.name for f in Port._meta.fields]


class PriceAdmin(AdminMixin):
    list_display = [f.name for f in Price._meta.fields]


admin.site.register(Region, RegionAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(Price, PriceAdmin)
