from vehicles.models import Vehicle, VehiclePurchase, VehicleDetail, VehicleRegistration
from django.utils import timezone
import random

def run():
    print("Seeding vehicle data...")

    brands = ["Toyota", "Honda", "Nissan", "Ford", "BMW", "Suzuki", "Hyundai", "Kia", "Mazda", "Chevrolet"]
    models = ["Corolla", "Civic", "Sunny", "Focus", "320i", "Swift", "Elantra", "Sportage", "Axela", "Cruze"]
    fuel_types = ["Petrol", "Diesel", "Hybrid"]
    colors = ["White", "Black", "Silver", "Blue", "Red", "Grey"]
    countries = ["Japan", "Germany", "USA", "Korea"]

    today = timezone.now().date()
    detail_count = 0

    for i in range(50):
        brand = random.choice(brands)
        model = random.choice(models)
        condition = random.choice(["New", "Used"])
        year = random.randint(2010, 2023)

        vehicle = Vehicle.objects.create(
            brand=brand,
            model=model,
            vehicle_class="Sedan",
            year=year,
            cylinder_capacity=random.choice([1300, 1500, 1800, 2000]),
            fuel_type=random.choice(fuel_types),
            origin_country=random.choice(countries),
            wheel_base=random.randint(2500, 2800),
            seating_capacity=5,
            condition=condition,
            availability=(condition == "New"),
            created_at=today
        )

        quantity = 1 if condition == "Used" else random.randint(1, 5)

        VehiclePurchase.objects.create(
            vehicle=vehicle,
            supplier_name=f"Supplier_{i}",
            supplier_location=f"City_{i % 10}",
            unit_price=random.randint(2000000, 6000000),
            quantity=quantity,
            purchase_date=today
        )

        for q in range(quantity):
            detail_count += 1
            chassis = f"CHS{100000 + detail_count}"
            price = random.randint(2500000, 7000000)  # 💵 Random price per unit

            detail = VehicleDetail.objects.create(
                chassis_no=chassis,
                vehicle=vehicle,
                engine_no=f"ENG{100000 + detail_count}",
                color=random.choice(colors),
                price=price,  # 👈 MUST ADD price now
                modification="None"
            )

            if condition == "Used":
                VehicleRegistration.objects.create(
                    chassis_no=detail,
                    license_plate=f"WP-{random.randint(1000, 9999)}",
                    owner_name=f"Owner_{detail_count}",
                    owner_location=f"Town_{detail_count % 20}",
                    register_date=today.replace(year=today.year - random.randint(1, 5)),
                    special_note="Imported" if random.random() > 0.5 else None
                )

    print("✅ Seeding complete.")
