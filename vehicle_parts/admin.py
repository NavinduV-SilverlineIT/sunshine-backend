from django.contrib import admin
from .models import Vehicle, VehicleParts, VehicleParts_Purchases, VehicleParts_Sales, VehicleParts_SaleItems

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'class_name', 'year', 'origin_country', 'created_at')
    search_fields = ('brand', 'model', 'class_name', 'year')
    list_filter = ('brand', 'year', 'origin_country')

@admin.register(VehicleParts)
class VehiclePartsAdmin(admin.ModelAdmin):
    list_display = ('part_name', 'part_no', 'vehicle', 'made_in', 'warranty', 'stock_place', 'created_at')
    search_fields = ('part_name', 'part_no', 'vehicle__brand', 'vehicle__model')
    list_filter = ('vehicle__brand', 'made_in', 'warranty')

@admin.register(VehicleParts_Purchases)
class VehiclePartsPurchasesAdmin(admin.ModelAdmin):
    list_display = ('vp', 'supplier_name', 'quantity', 'purchase_price', 'selling_price', 'purchase_date')
    search_fields = ('vp__part_name', 'supplier_name')
    list_filter = ('purchase_date', 'supplier_name')

class VehiclePartsSaleItemsInline(admin.TabularInline):
    model = VehicleParts_SaleItems
    extra = 1
    fields = ('vp', 'quantity', 'sold_price')

@admin.register(VehicleParts_Sales)
class VehiclePartsSalesAdmin(admin.ModelAdmin):
    list_display = ('vps_id', 'customer_name', 'place', 'sale_date', 'created_at')
    search_fields = ('customer_name', 'place')
    list_filter = ('sale_date', 'place')
    inlines = [VehiclePartsSaleItemsInline]

@admin.register(VehicleParts_SaleItems)
class VehiclePartsSaleItemsAdmin(admin.ModelAdmin):
    list_display = ('sale', 'vp', 'quantity', 'sold_price', 'created_at')
    search_fields = ('sale__customer_name', 'vp__part_name')
    list_filter = ('sale__sale_date',)