from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
