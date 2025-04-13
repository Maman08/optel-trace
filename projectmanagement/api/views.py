from django.shortcuts import render
from rest_framework import viewsets,permissions,filters
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
# Create your views here.

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.created_by == request.user

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name','created_at']



class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'created_at']
    
    def get_queryset(self):
        """
        Optionally restricts the returned products by filtering against
        query parameters in the URL.
        """
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__id=category)
        
        available = self.request.query_params.get('available')
        if available is not None:
            is_available = True if available.lower() == 'true' else False
            queryset = queryset.filter(is_available=is_available)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)































