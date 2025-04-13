from rest_framework import serializers
from .models import Product , Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at']
        
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at','created_by']        