from rest_framework import serializers
from .models import Vehicle, VehicleParts, VehicleParts_Purchases, VehicleParts_Sales
from django.utils import timezone

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_id', 'brand', 'model', 'class_name', 'year',
            'origin_country', 'created_at'
        ]
        read_only_fields = ['vehicle_id', 'created_at']

class VehiclePartsPurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleParts_Purchases
        fields = [
            'vpp_id', 'supplier_name', 'arrival_method', 'purchase_price',
            'quantity', 'selling_price', 'purchase_date'
        ]
        read_only_fields = ['vpp_id']

class VehiclePartsSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleParts_Sales
        fields = [
            'vps_id', 'customer_name', 'place', 'quantity',
            'sold_price', 'sold_date'
        ]
        read_only_fields = ['vps_id']

class VehiclePartsSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source='vehicle',
        write_only=True,
        required=True
    )
    purchases = VehiclePartsPurchasesSerializer(many=True, read_only=True)
    sales = VehiclePartsSalesSerializer(many=True, read_only=True)
    stock_status = serializers.SerializerMethodField()
    stock_quantity = serializers.SerializerMethodField()
    new_purchases = VehiclePartsPurchasesSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = VehicleParts
        fields = [
            'vp_id', 'vehicle', 'vehicle_id', 'part_name', 'part_no',
            'bn_rc', 'mf_date', 'warranty', 'made_in', 'stock_place',
            'created_at', 'purchases', 'sales', 'stock_status',
            'stock_quantity', 'new_purchases'
        ]
        read_only_fields = ['vp_id', 'created_at', 'purchases', 'sales', 'stock_status', 'stock_quantity']

    def get_stock_status(self, obj):
        return obj.stock_status()

    def get_stock_quantity(self, obj):
        return obj.stock_quantity()

    def validate(self, data):
        # Ensure vehicle_id is provided
        if 'vehicle' not in data and not self.instance:
            raise serializers.ValidationError("Vehicle is required for vehicle parts")
        
        # Validate part_no uniqueness for the same vehicle
        vehicle = data.get('vehicle', self.instance.vehicle if self.instance else None)
        part_no = data.get('part_no', self.instance.part_no if self.instance else None)
        
        if vehicle and part_no:
            existing_part = VehicleParts.objects.filter(
                vehicle=vehicle,
                part_no=part_no
            ).exclude(pk=self.instance.pk if self.instance else None).first()
            
            if existing_part:
                raise serializers.ValidationError(
                    f"Part number {part_no} already exists for this vehicle"
                )
        
        return data

    def create(self, validated_data):
        new_purchases = validated_data.pop('new_purchases', [])
        vehicle_part = VehicleParts.objects.create(**validated_data)

        for purchase_data in new_purchases:
            VehicleParts_Purchases.objects.create(vp=vehicle_part, **purchase_data)

        return vehicle_part

    def update(self, instance, validated_data):
        new_purchases = validated_data.pop('new_purchases', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for purchase_data in new_purchases:
            VehicleParts_Purchases.objects.create(vp=instance, **purchase_data)

        return instance