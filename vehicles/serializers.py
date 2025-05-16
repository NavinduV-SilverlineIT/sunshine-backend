# vehicles/serializers.py

from rest_framework import serializers
from .models import Vehicle, VehiclePurchase, VehicleDetail, VehicleSale, VehicleRegistration

class VehiclePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePurchase
        fields = '__all__'

class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDetail
        fields = '__all__'

class VehicleSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleSale
        fields = '__all__'

class VehicleRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRegistration
        fields = '__all__'

# 👇 Master serializer that nests the others
class VehicleSerializer(serializers.ModelSerializer):
    purchases = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            'id', 'brand', 'model', 'vehicle_class', 'year', 'cylinder_capacity',
            'fuel_type', 'origin_country', 'wheel_base', 'seating_capacity',
            'condition', 'availability', 'created_at', 'purchases', 'details'
        ]

    def get_purchases(self, obj):
        purchases = VehiclePurchase.objects.filter(vehicle=obj)
        return VehiclePurchaseSerializer(purchases, many=True).data

    def get_details(self, obj):
        details = VehicleDetail.objects.filter(vehicle=obj)
        return VehicleDetailWithExtrasSerializer(details, many=True).data

# 👇 Wrap detail with nested sale + registration info
class VehicleDetailWithExtrasSerializer(serializers.ModelSerializer):
    sale = serializers.SerializerMethodField()
    registration = serializers.SerializerMethodField()

    class Meta:
        model = VehicleDetail
        fields = [
            'chassis_no',
            'vehicle',
            'engine_no',
            'color',
            'modification',
            'price',
            'sale',
            'registration'
        ]

    def get_sale(self, obj):
        sale = VehicleSale.objects.filter(chassis_no=obj).first()
        return VehicleSaleSerializer(sale).data if sale else None

    def get_registration(self, obj):
        reg = VehicleRegistration.objects.filter(chassis_no=obj).first()
        return VehicleRegistrationSerializer(reg).data if reg else None



# from rest_framework import serializers
# from .models import Vehicle, VehiclePurchase, VehicleDetail, VehicleSale, VehicleRegistration

# class VehicleRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleRegistration
#         fields = ['vr_id', 'license_plate', 'owner_name', 'owner_location', 'register_date', 'special_note', 'chassis_no']
#         extra_kwargs = {
#             'vr_id': {'source': 'vr_id'},
#             'chassis_no': {'source': 'chassis_no_id'}  # Map ForeignKey to chassis_no
#         }

# class VehicleSaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleSale
#         fields = ['id', 'customer_name', 'customer_location', 'sold_price', 'sold_date', 'chassis_no']
#         extra_kwargs = {
#             'chassis_no': {'source': 'chassis_no_id'}  # Map ForeignKey to chassis_no
#         }

# class VehicleDetailSerializer(serializers.ModelSerializer):
#     sale = VehicleSaleSerializer(allow_null=True)
#     registration = VehicleRegistrationSerializer(allow_null=True)

#     class Meta:
#         model = VehicleDetail
#         fields = ['chassis_no', 'vehicle', 'engine_no', 'color', 'modification', 'sale', 'registration']

# class VehiclePurchaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehiclePurchase
#         fields = ['id', 'supplier_name', 'supplier_location', 'unit_price', 'quantity', 'purchase_date', 'vehicle']

# class VehicleSerializer(serializers.ModelSerializer):
#     purchases = VehiclePurchaseSerializer(source='vehiclepurchase_set', many=True)
#     details = VehicleDetailSerializer(source='vehicledetail_set', many=True)
#     quantity = serializers.SerializerMethodField()
#     status = serializers.SerializerMethodField()

#     class Meta:
#         model = Vehicle
#         fields = [
#             'id', 'brand', 'model', 'vehicle_class', 'year', 'cylinder_capacity', 'fuel_type',
#             'origin_country', 'wheel_base', 'seating_capacity', 'condition', 'availability',
#             'created_at', 'purchases', 'details', 'quantity', 'status'
#         ]

#     def get_quantity(self, obj):
#         total_quantity = sum(purchase.quantity for purchase in obj.vehiclepurchase_set.all())
#         sold_quantity = sum(1 for detail in obj.vehicledetail_set.all() if detail.vehiclesale_set.exists())
#         return total_quantity - sold_quantity

#     def get_status(self, obj):
#         has_in_stock = any(not detail.vehiclesale_set.exists() for detail in obj.vehicledetail_set.all())
#         return 'In Stock' if has_in_stock else 'Sold'