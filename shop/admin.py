from django.contrib import admin
from shop.models import EstateApplication, AdditionalEstateImage, EstatePurchaseOrder

from shop.utils import make_thumbnail, apply_discount


class EstateApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ['discounted_price', ]


admin.site.register(AdditionalEstateImage)
admin.site.register(EstatePurchaseOrder)
admin.site.register(EstateApplication, EstateApplicationAdmin)
