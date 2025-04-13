from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=255)
    description= models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name    


class Product(models.Model):
    name= models.CharField(max_length=255)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    stock=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name