from rest_framework import serializers
from shop.models import EstateApplication, AdditionalEstateImage, EstatePurchaseOrder


class EstateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateApplication
        fields = '__all__'


class EstateAdditionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalEstateImage
        fields = '__all__'


class EstatePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatePurchaseOrder
        fields = '__all__'
