from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import EstateApplication, AdditionalEstateImage, EstatePurchaseOrder
from shop.pagination import SmallResultsSetPagination
from shop.serializers import \
    EstateApplicationSerializer, \
    EstatePurchaseOrderSerializer, \
    EstateAdditionalImageSerializer


class EstateListView(ReadOnlyModelViewSet):
    queryset = EstateApplication.objects.all()
    serializer_class = EstateApplicationSerializer
    permission_classes = [AllowAny, ]
    pagination_class = SmallResultsSetPagination


class AdditionalEstateImageListView(ReadOnlyModelViewSet):
    queryset = AdditionalEstateImage.objects.all()
    serializer_class = EstateAdditionalImageSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estate', ]


class EstateOrderCreateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = EstatePurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            EstatePurchaseOrder.send_estate_order_email(request.data)
            return Response(status=200)
        else:
            return Response(status=400)
