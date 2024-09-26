from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from users.api_exception import GenericException, success_response, standard_response, generic_middleware_exception
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache

class InventoryItemViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request):
        try:
            serializer = InventoryItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print("Item has been created")
                return success_response(data=serializer.data, message="Item created successfully")
            else:
                raise GenericException(error_message="Invalid data provided", status=400)
        except GenericException as e:
            return Response(e.detail, status=e.status_code)
        except Exception as e:
            return generic_middleware_exception(exc=e, context={"view": self})

    def retrieve(self, request, pk=None):
        try:
            cache_key = f"inventory_item_{pk}"
            item = cache.get(cache_key)  # Try to fetch from cache
            if not item:
                # If cache miss, retrieve from the database
                item = InventoryItem.objects.get(inventory_id=pk)
                serializer = InventoryItemSerializer(item)
                # Store the serialized item in cache
                cache.set(cache_key, serializer.data, timeout=60 * 15)  # Cache for 15 minutes
            else:
                # If cached, no need to serialize again
                serializer = InventoryItemSerializer(item)
                print("Retrived from cache Item")
                
            return success_response(data=serializer.data, message="Item retrieved successfully")
        except InventoryItem.DoesNotExist:
            raise GenericException(error_message="Item not found", status=404)
        except Exception as e:
            return generic_middleware_exception(exc=e, context={"view": self})

    def update(self, request, pk=None):
        try:
            item = InventoryItem.objects.get(inventory_id=pk)
            serializer = InventoryItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Invalidate the cache for this item since it has been updated
                cache_key = f"inventory_item_{pk}"
                cache.delete(cache_key)
                print("Updated the cache Item")

                return success_response(data=serializer.data, message="Item updated successfully")
            else:
                raise GenericException(error_message="Invalid data provided", status=400)
        except InventoryItem.DoesNotExist:
            raise GenericException(error_message="Item not found", status=404)
        except Exception as e:
            return generic_middleware_exception(exc=e, context={"view": self})

    def destroy(self, request, pk=None):
        try:
            item = InventoryItem.objects.get(inventory_id=pk)
            item.delete()
            # Invalidate the cache for this item since it has been deleted
            cache_key = f"inventory_item_{pk}"
            cache.delete(cache_key)
            print("Deleted the cache Item")
            return success_response(message="Item deleted successfully")
        except InventoryItem.DoesNotExist:
            raise GenericException(error_message="Item not found", status=404)
        except Exception as e:
            return generic_middleware_exception(exc=e, context={"view": self})
