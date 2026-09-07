from django.db import models
from django.utils import timezone
import random
import string

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"

class LaundryService(models.Model):
    CATEGORY_CHOICES = [
        ('WASH_FOLD', 'Wash & Fold'),
        ('WASH_IRON', 'Wash & Iron'),
        ('DRY_CLEAN', 'Dry Cleaning'),
        ('IRON_ONLY', 'Ironing Only'),
        ('EXPRESS', 'Express Care'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='WASH_FOLD')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg', help_text="Unit of measurement e.g. kg, piece, pair")
    description = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, default='bi-basket', help_text="Bootstrap/FontAwesome Icon class")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (${self.price_per_unit}/{self.unit})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('READY', 'Ready for Pickup'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partially Paid'),
    ]

    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='UNPAID')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            prefix = "ORD"
            random_str = ''.join(random.choices(string.digits, k=6))
            self.order_number = f"{prefix}-{random_str}"
        super().save(*args, **kwargs)

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(LaundryService, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1.0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.service and not self.unit_price:
            self.unit_price = self.service.price_per_unit
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        if self.order_id:
            self.order.calculate_total()

    def __str__(self):
        return f"{self.quantity} x {self.service.name if self.service else 'Item'} (${self.subtotal})"
