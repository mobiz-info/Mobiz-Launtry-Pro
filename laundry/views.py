from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, Q
from django.contrib import messages
from rest_framework import viewsets, serializers
from .models import Customer, LaundryService, Order, OrderItem

# --- DRF Serializers ---
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class LaundryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryService
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'service', 'service_name', 'quantity', 'unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'customer_name', 'status', 'payment_status', 'total_amount', 'notes', 'due_date', 'created_at', 'items']

# --- DRF ViewSets ---
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class LaundryServiceViewSet(viewsets.ModelViewSet):
    queryset = LaundryService.objects.all()
    serializer_class = LaundryServiceSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# --- Template Views ---
def dashboard_view(request):
    """Render empty white screen dashboard layout."""
    return render(request, 'laundry/dashboard.html')

def master_settings_view(request):
    """Render Master Settings page with Laundry Services and Company Settings."""
    services = LaundryService.objects.all()
    return render(request, 'laundry/master_settings.html', {'services': services})

def services_list_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price_per_unit')
        unit = request.POST.get('unit', 'kg')
        description = request.POST.get('description', '')

        if name and price:
            LaundryService.objects.create(
                name=name,
                category=category,
                price_per_unit=price,
                unit=unit,
                description=description
            )
            messages.success(request, f"Master service '{name}' created successfully!")
            return redirect('master_settings')

    services = LaundryService.objects.all()
    return render(request, 'laundry/master_settings.html', {'services': services})

def orders_list_view(request):
    orders = Order.objects.select_related('customer').all()
    return render(request, 'laundry/dashboard.html', {'orders': orders})

def customers_list_view(request):
    customers = Customer.objects.all()
    return render(request, 'laundry/dashboard.html', {'customers': customers})
