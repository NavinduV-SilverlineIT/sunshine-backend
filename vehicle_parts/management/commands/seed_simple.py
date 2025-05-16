from django.core.management.base import BaseCommand
from django.utils import timezone
from vehicle_parts.models import Vehicle, VehicleParts, VehicleParts_Purchases, VehicleParts_Sales, VehicleParts_SaleItems
from decimal import Decimal
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with a simple set of sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        VehicleParts_SaleItems.objects.all().delete()
        VehicleParts_Sales.objects.all().delete()
        VehicleParts_Purchases.objects.all().delete()
        VehicleParts.objects.all().delete()
        Vehicle.objects.all().delete()

        # Fixed set of vehicles
        vehicles_data = [
            {'brand': 'Toyota', 'model': 'Corolla', 'class_name': 'Sedan', 'year': 2022},
            {'brand': 'Honda', 'model': 'Civic', 'class_name': 'Sedan', 'year': 2021},
            {'brand': 'Nissan', 'model': 'X-Trail', 'class_name': 'SUV', 'year': 2023},
            {'brand': 'Mitsubishi', 'model': 'Pajero', 'class_name': 'SUV', 'year': 2020},
            {'brand': 'Suzuki', 'model': 'Swift', 'class_name': 'Hatchback', 'year': 2022},
            {'brand': 'Toyota', 'model': 'RAV4', 'class_name': 'SUV', 'year': 2021},
            {'brand': 'Honda', 'model': 'CR-V', 'class_name': 'SUV', 'year': 2023},
            {'brand': 'Nissan', 'model': 'Patrol', 'class_name': 'SUV', 'year': 2020},
            {'brand': 'Mitsubishi', 'model': 'Lancer', 'class_name': 'Sedan', 'year': 2022},
            {'brand': 'Suzuki', 'model': 'Jimny', 'class_name': 'SUV', 'year': 2023},
        ]

        # Fixed set of parts per vehicle type
        parts_data = {
            'Sedan': [
                {'name': 'Engine Oil Filter', 'part_no': 1001},
                {'name': 'Air Filter', 'part_no': 1002},
                {'name': 'Brake Pad Set', 'part_no': 1003},
                {'name': 'Spark Plug Set', 'part_no': 1004},
                {'name': 'Timing Belt', 'part_no': 1005},
            ],
            'SUV': [
                {'name': 'Suspension Kit', 'part_no': 2001},
                {'name': '4WD Transfer Case', 'part_no': 2002},
                {'name': 'Off-road Tire Set', 'part_no': 2003},
                {'name': 'Skid Plate', 'part_no': 2004},
                {'name': 'Winch Kit', 'part_no': 2005},
            ],
            'Hatchback': [
                {'name': 'Fuel Pump', 'part_no': 3001},
                {'name': 'Clutch Kit', 'part_no': 3002},
                {'name': 'CV Joint', 'part_no': 3003},
                {'name': 'Radiator', 'part_no': 3004},
                {'name': 'Alternator', 'part_no': 3005},
            ]
        }

        # Create vehicles
        vehicles = []
        for data in vehicles_data:
            vehicle = Vehicle.objects.create(
                brand=data['brand'],
                model=data['model'],
                class_name=data['class_name'],
                year=data['year'],
                origin_country='Japan'
            )
            vehicles.append(vehicle)
            self.stdout.write(f'Created vehicle: {vehicle}')

        # Create parts for each vehicle
        parts = []
        for vehicle in vehicles:
            vehicle_parts = parts_data[vehicle.class_name]
            for part_data in vehicle_parts:
                part = VehicleParts.objects.create(
                    vehicle=vehicle,
                    part_name=part_data['name'],
                    part_no=part_data['part_no'],
                    bn_rc=f"BN{part_data['part_no']}",
                    mf_date=timezone.now().date() - timedelta(days=random.randint(0, 365)),
                    warranty=random.randint(6, 36),
                    made_in='Japan',
                    stock_place='Warehouse A'
                )
                parts.append(part)
                self.stdout.write(f'Created part: {part}')

        # Create purchases for each part
        suppliers = ['Auto Parts Co.', 'Global Motors', 'Tech Auto']
        for part in parts:
            # Create 2 purchases for each part
            for _ in range(2):
                quantity = random.randint(5, 20)
                purchase_price = Decimal(random.randint(1000, 5000))
                selling_price = purchase_price * Decimal('1.3')  # 30% markup
                
                VehicleParts_Purchases.objects.create(
                    vp=part,
                    supplier_name=random.choice(suppliers),
                    arrival_method='Air Freight',
                    purchase_price=purchase_price,
                    quantity=quantity,
                    selling_price=selling_price,
                    purchase_date=timezone.now().date() - timedelta(days=random.randint(0, 30))
                )
            self.stdout.write(f'Created purchases for part: {part}')

        # Create sales
        customers = ['John Smith', 'Sarah Johnson', 'Mike Brown']
        places = ['Colombo', 'Kandy', 'Galle']

        for _ in range(10):  # Create 10 sales
            sale = VehicleParts_Sales.objects.create(
                customer_name=random.choice(customers),
                place=random.choice(places),
                sale_date=timezone.now().date() - timedelta(days=random.randint(0, 15))
            )
            
            # Add 2 items to each sale
            sale_parts = random.sample(parts, 2)
            
            for part in sale_parts:
                quantity = random.randint(1, 3)
                sold_price = part.purchases.first().selling_price * Decimal(str(random.uniform(0.9, 1.1)))
                
                VehicleParts_SaleItems.objects.create(
                    sale=sale,
                    vp=part,
                    quantity=quantity,
                    sold_price=sold_price
                )
            self.stdout.write(f'Created sale with items: {sale}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!')) 