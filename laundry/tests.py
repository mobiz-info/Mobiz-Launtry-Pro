from django.test import TestCase, Client
from django.urls import reverse
from .models import Customer, LaundryService, Order, OrderItem

class LaundryModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="John Doe",
            phone="+1234567890",
            email="john@example.com"
        )
        self.service = LaundryService.objects.create(
            name="Shirt Wash",
            category="WASH_FOLD",
            price_per_unit=5.00,
            unit="piece"
        )

    def test_customer_creation(self):
        self.assertEqual(str(self.customer), "John Doe (+1234567890)")

    def test_order_creation(self):
        order = Order.objects.create(customer=self.customer)
        self.assertTrue(order.order_number.startswith("ORD-"))

class LaundryViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_url(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_master_settings_url(self):
        response = self.client.get(reverse('master_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Master Settings")

    def test_api_orders_endpoint(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
