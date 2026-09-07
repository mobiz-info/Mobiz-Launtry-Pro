from django.core.management.base import BaseCommand
from laundry.models import Customer, LaundryService, Order, OrderItem
import random

class Command(BaseCommand):
    help = 'Seeds initial sample data for Mobiz Laundry Studio'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data for Mobiz Laundry...'))

        # 1. Services
        services_data = [
            {'name': 'Everyday Wash & Fold', 'category': 'WASH_FOLD', 'price_per_unit': 3.50, 'unit': 'kg', 'icon_name': 'bi-basket-fill', 'description': 'Standard wash, tumble dry, and neat folding.'},
            {'name': 'Executive Suit Dry Clean', 'category': 'DRY_CLEAN', 'price_per_unit': 18.00, 'unit': 'piece', 'icon_name': 'bi-person-badge', 'description': 'Premium eco dry cleaning for 2-piece suits.'},
            {'name': 'Steam Ironing & Hanger', 'category': 'IRON_ONLY', 'price_per_unit': 2.00, 'unit': 'piece', 'icon_name': 'bi-wind', 'description': 'Crisp steam press on hangers.'},
            {'name': 'Gentle Silk & Dress Clean', 'category': 'DRY_CLEAN', 'price_per_unit': 14.50, 'unit': 'piece', 'icon_name': 'bi-stars', 'description': 'Delicate care for silk dresses and gowns.'},
            {'name': 'Bedding & Comforter Care', 'category': 'WASH_FOLD', 'price_per_unit': 12.00, 'unit': 'item', 'icon_name': 'bi-box-seam', 'description': 'Heavy duty wash and sanitization for duvet & blankets.'},
            {'name': 'Express 3-Hour Wash & Iron', 'category': 'EXPRESS', 'price_per_unit': 6.00, 'unit': 'kg', 'icon_name': 'bi-lightning-charge-fill', 'description': 'Priority turnaround service.'},
        ]

        services = []
        for item in services_data:
            s, _ = LaundryService.objects.get_or_create(
                name=item['name'],
                defaults=item
            )
            services.append(s)

        self.stdout.write(f'Created {len(services)} services.')

        # 2. Customers
        customers_data = [
            {'name': 'Alex Morgan', 'phone': '+1 (555) 234-5678', 'email': 'alex.m@example.com', 'address': '452 Park Avenue, Apt 4B'},
            {'name': 'Sarah Jenkins', 'phone': '+1 (555) 876-5432', 'email': 'sarah.j@example.com', 'address': '789 Sunset Blvd, Suite 12'},
            {'name': 'David Chen', 'phone': '+1 (555) 345-6789', 'email': 'd.chen@example.com', 'address': '101 Tech Center Dr'},
            {'name': 'Emma Watson', 'phone': '+1 (555) 901-2345', 'email': 'emma.w@example.com', 'address': '12 Rose Gardens, Block C'},
        ]

        customers = []
        for cdata in customers_data:
            c, _ = Customer.objects.get_or_create(
                phone=cdata['phone'],
                defaults=cdata
            )
            customers.append(c)

        self.stdout.write(f'Created {len(customers)} customers.')

        # 3. Orders
        statuses = ['PENDING', 'IN_PROGRESS', 'READY', 'DELIVERED']
        payments = ['PAID', 'UNPAID', 'PARTIAL']

        if Order.objects.count() == 0:
            for customer in customers:
                for _ in range(random.randint(1, 2)):
                    order = Order.objects.create(
                        customer=customer,
                        status=random.choice(statuses),
                        payment_status=random.choice(payments),
                        notes="Handled with care. Ring bell on delivery."
                    )
                    # Add 2 random items
                    selected_services = random.sample(services, k=2)
                    for svc in selected_services:
                        qty = random.choice([1.0, 2.0, 3.5, 5.0])
                        OrderItem.objects.create(
                            order=order,
                            service=svc,
                            quantity=qty,
                            unit_price=svc.price_per_unit
                        )
            self.stdout.write(self.style.SUCCESS(f'Created sample orders successfully! Total orders: {Order.objects.count()}'))

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
