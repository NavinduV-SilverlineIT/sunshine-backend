
from vehicles.models import Vehicle, VehicleDetail, VehicleSale
from django.utils import timezone
import random

def run():
    print("Seeding vehicle sales for existing 20 vehicles...")

    today = timezone.now().date()
    vehicles = Vehicle.objects.all().order_by('id')[:20]

    sale_count = 0

    for vehicle in vehicles:
        details = VehicleDetail.objects.filter(vehicle=vehicle)

        if not details.exists():
            continue

        # Randomly choose 1 or more details to mark as sold
        to_sell = random.sample(list(details), k=random.randint(1, min(2, len(details))))

        for detail in to_sell:
            # Only add sale if not already sold
            if not VehicleSale.objects.filter(chassis_no=detail).exists():
                VehicleSale.objects.create(
                    chassis_no=detail,
                    customer_name=f"Customer_{sale_count + 1}",
                    customer_location=f"City_{random.randint(1, 20)}",
                    sold_price=random.randint(2500000, 7000000),
                    sold_date=today
                )
                sale_count += 1

        # Mark vehicle as unavailable if any units sold
        vehicle.availability = False
        vehicle.save()

    print(f"✅ Added sales for {sale_count} vehicle details.")
