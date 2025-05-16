from rest_framework import viewsets
from .models import Vehicle, VehiclePurchase, VehicleDetail, VehicleSale, VehicleRegistration
from .serializers import (
    VehicleSerializer, VehiclePurchaseSerializer,
    VehicleDetailSerializer, VehicleSaleSerializer, VehicleRegistrationSerializer
)

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehiclePurchaseViewSet(viewsets.ModelViewSet):
    queryset = VehiclePurchase.objects.all()
    serializer_class = VehiclePurchaseSerializer

class VehicleDetailViewSet(viewsets.ModelViewSet):
    queryset = VehicleDetail.objects.all()
    serializer_class = VehicleDetailSerializer

class VehicleSaleViewSet(viewsets.ModelViewSet):
    queryset = VehicleSale.objects.all()
    serializer_class = VehicleSaleSerializer

class VehicleRegistrationViewSet(viewsets.ModelViewSet):
    queryset = VehicleRegistration.objects.all()
    serializer_class = VehicleRegistrationSerializer



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.db.models import Q
# from .models import Vehicle, VehicleDetail
# from .serializers import VehicleSerializer
# import json

# class VehicleListView(APIView):
#     def get(self, request):
#         # Extract query parameters
#         page = int(request.query_params.get('page', 1))
#         page_size = int(request.query_params.get('page_size', 50))
#         sort = request.query_params.get('sort')
#         direction = request.query_params.get('direction', 'asc')
#         search = request.query_params.get('search')
#         brand = request.query_params.get('brand')
#         vehicle_class = request.query_params.get('vehicle_class')
#         condition = request.query_params.get('condition')
#         column_filters = request.query_params.get('column_filters')
#         tab = request.query_params.get('tab', 'all')

#         # Base queryset
#         queryset = Vehicle.objects.all()

#         # Apply tab filter
#         if tab == 'in_stock':
#             queryset = queryset.filter(vehicledetail__vehiclesale__isnull=True).distinct()
#         elif tab == 'sold':
#             queryset = queryset.filter(vehicledetail__vehiclesale__isnull=False).distinct()

#         # Apply master filters
#         if brand:
#             queryset = queryset.filter(brand__in=brand.split(','))
#         if vehicle_class:
#             queryset = queryset.filter(vehicle_class__in=vehicle_class.split(','))
#         if condition:
#             queryset = queryset.filter(condition__in=condition.split(','))

#         # Apply column filters
#         if column_filters:
#             column_filters = json.loads(column_filters)
#             if column_filters.get('brand'):
#                 queryset = queryset.filter(brand__icontains=column_filters['brand'])
#             if column_filters.get('model'):
#                 queryset = queryset.filter(model__icontains=column_filters['model'])
#             if column_filters.get('year'):
#                 queryset = queryset.filter(year__icontains=column_filters['year'])
#             if column_filters.get('condition'):
#                 queryset = queryset.filter(condition__icontains=column_filters['condition'])
#             # Quantity and status are computed fields, filter client-side or add custom logic
#             # Example for status
#             if column_filters.get('status'):
#                 if column_filters['status'].lower() == 'in stock':
#                     queryset = queryset.filter(vehicledetail__vehiclesale__isnull=True).distinct()
#                 elif column_filters['status'].lower() == 'sold':
#                     queryset = queryset.filter(vehicledetail__vehiclesale__isnull=False).distinct()

#         # Apply search
#         if search:
#             queryset = queryset.filter(Q(brand__icontains=search) | Q(model__icontains=search))

#         # Apply sorting
#         if sort:
#             sort_field = sort if direction == 'asc' else f'-{sort}'
#             queryset = queryset.order_by(sort_field)

#         # Pagination
#         total_count = queryset.count()
#         start = (page - 1) * page_size
#         end = start + page_size
#         queryset = queryset[start:end]

#         # Serialize data
#         serializer = VehicleSerializer(queryset, many=True)
#         return Response({
#             'results': serializer.data,
#             'count': total_count,
#         }, status=status.HTTP_200_OK)

# class FilterOptionsView(APIView):
#     def get(self, request):
#         # Fetch unique values for filters
#         brands = Vehicle.objects.values('brand').distinct()
#         vehicle_classes = Vehicle.objects.values('vehicle_class').distinct()
#         conditions = Vehicle.objects.values('condition').distinct()
#         return Response({
#             'brand': [item['brand'] for item in brands],
#             'vehicle_class': [item['vehicle_class'] for item in vehicle_classes],
#             'condition': [item['condition'] for item in conditions],
#         }, status=status.HTTP_200_OK)