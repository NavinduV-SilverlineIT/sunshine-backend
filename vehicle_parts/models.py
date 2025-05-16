from django.db import models
from django.db.models import Sum
from django.utils import timezone

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)  # Renamed to avoid Python keyword 'class'
    year = models.PositiveIntegerField()
    origin_country = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class VehicleParts(models.Model):
    vp_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='parts')
    part_name = models.CharField(max_length=255)
    part_no = models.IntegerField()
    bn_rc = models.CharField(max_length=50)
    mf_date = models.DateField(blank=True, null=True)
    warranty = models.PositiveIntegerField()
    made_in = models.CharField(max_length=50)
    stock_place = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True, editable=False)

    def stock_status(self):
        total_purchased = self.purchases.aggregate(total=Sum('quantity'))['total'] or 0
        total_sold = self.sale_items.aggregate(total=Sum('quantity'))['total'] or 0
        return 'In Stock' if total_purchased > total_sold else 'Out of Stock'

    def stock_quantity(self):
        total_purchased = self.purchases.aggregate(total=Sum('quantity'))['total'] or 0
        total_sold = self.sale_items.aggregate(total=Sum('quantity'))['total'] or 0
        return total_purchased - total_sold

    class Meta:
        verbose_name = 'Vehicle Part'
        verbose_name_plural = 'Vehicle Parts'
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'part_name'], name='unique_vehicle_part')
        ]

    def __str__(self):
        return f"{self.part_name} for {self.vehicle}"

class VehicleParts_Purchases(models.Model):
    vpp_id = models.AutoField(primary_key=True)
    vp = models.ForeignKey(VehicleParts, on_delete=models.CASCADE, related_name='purchases')
    supplier_name = models.CharField(max_length=100)
    arrival_method = models.CharField(max_length=255, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=15, decimal_places=2)  # Intended selling price
    purchase_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Vehicle Parts Purchase'
        verbose_name_plural = 'Vehicle Parts Purchases'

    def __str__(self):
        return f"Purchase {self.vpp_id} of {self.vp.part_name}"

class VehicleParts_Sales(models.Model):
    vps_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    place = models.CharField(max_length=255, blank=True, null=True)  # Delivery/buyer location
    sale_date = models.DateField(default=timezone.now)
    created_at = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Vehicle Parts Sale'
        verbose_name_plural = 'Vehicle Parts Sales'

    def __str__(self):
        return f"Sale {self.vps_id} to {self.customer_name}"

class VehicleParts_SaleItems(models.Model):
    sale = models.ForeignKey(VehicleParts_Sales, on_delete=models.CASCADE, related_name='items')
    vp = models.ForeignKey(VehicleParts, on_delete=models.CASCADE, related_name='sale_items')
    quantity = models.PositiveIntegerField()
    sold_price = models.DecimalField(max_digits=15, decimal_places=2)  # Actual price paid
    created_at = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Vehicle Parts Sale Item'
        verbose_name_plural = 'Vehicle Parts Sale Items'
        constraints = [
            models.UniqueConstraint(fields=['sale', 'vp'], name='unique_sale_part')
        ]

    def __str__(self):
        return f"Sale item of {self.vp.part_name} in sale {self.sale.vps_id}"