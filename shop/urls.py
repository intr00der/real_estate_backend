from django.urls import path

from rest_framework import routers

from shop.views import EstateListView,\
    AdditionalEstateImageListView,\
    EstateOrderCreateView

router = routers.DefaultRouter()
router.register(r'estate-list', EstateListView, basename='estate-list')
router.register(r'additional-images', AdditionalEstateImageListView, basename='additional-images')

urlpatterns = [
    path('estates/orders/create/', EstateOrderCreateView.as_view(), name='estate_image_list'),
]
