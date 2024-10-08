from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore

# Custom User Model
class CustomUser(AbstractUser):
  fullname = models.CharField(max_length=50, blank=True, null=True)
  phone = models.CharField(max_length=15, blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  role = models.CharField(max_length=50, blank=True, null=True, default="user") 
  
  def __str__(self):
    return self.username

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=800)
    description = models.TextField()

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    img = models.CharField(max_length=900, default='')
    stock = models.IntegerField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('complete', 'Complete'),
        ('rejected', 'Rejected'),
    ]
     
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
