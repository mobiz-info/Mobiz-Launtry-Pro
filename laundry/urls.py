from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/customers', views.CustomerViewSet)
router.register(r'api/services', views.LaundryServiceViewSet)
router.register(r'api/orders', views.OrderViewSet)

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('master-settings/', views.master_settings_view, name='master_settings'),
    path('services/', views.services_list_view, name='services_list'),
    
    # API endpoints
    path('', include(router.urls)),
]
