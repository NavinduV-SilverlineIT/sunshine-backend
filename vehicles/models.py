from django.db import models

class Vehicle(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_class = models.CharField(max_length=50)
    year = models.IntegerField()
    cylinder_capacity = models.IntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=50, null=True, blank=True)
    wheel_base = models.IntegerField(null=True, blank=True)
    seating_capacity = models.IntegerField(null=True, blank=True)
    condition = models.CharField(max_length=50)
    availability = models.BooleanField()
    created_at = models.DateField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class VehiclePurchase(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=100)
    supplier_location = models.CharField(max_length=200, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField(default=1)
    purchase_date = models.DateField()

    def __str__(self):
        return f"Purchase of {self.vehicle} x{self.quantity} from {self.supplier_name}"


class VehicleDetail(models.Model):
    chassis_no = models.CharField(primary_key=True, max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    engine_no = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    modification = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.chassis_no} ({self.vehicle})"


class VehicleSale(models.Model):
    chassis_no = models.ForeignKey(VehicleDetail, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_location = models.CharField(max_length=200, blank=True, null=True)
    sold_price = models.DecimalField(max_digits=15, decimal_places=2)
    sold_date = models.DateField()

    def __str__(self):
        return f"Sold {self.chassis_no} to {self.customer_name} on {self.sold_date}"


class VehicleRegistration(models.Model):
    vr_id = models.AutoField(primary_key=True)
    chassis_no = models.ForeignKey(VehicleDetail, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=30)
    owner_name = models.CharField(max_length=200)
    owner_location = models.CharField(max_length=50)
    register_date = models.DateField()
    special_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reg {self.license_plate} for {self.chassis_no}"
