from rest_framework import viewsets
from .models import VehicleParts, VehicleParts_Purchases, VehicleParts_SaleItems
from .serializers import VehiclePartsSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class VehiclePartsViewSet(viewsets.ModelViewSet):
    queryset = VehicleParts.objects.all()
    serializer_class = VehiclePartsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'vp_id'

    def get_queryset(self):
        return VehicleParts.objects.prefetch_related('purchases', 'sale_items', 'sale_items__sale').all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Delete related purchases and sale items first
            VehicleParts_Purchases.objects.filter(vp=instance).delete()
            VehicleParts_SaleItems.objects.filter(vp=instance).delete()
            # Then delete the vehicle part
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)