"""Models for the e-commerce application."""
from io import BytesIO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

class User(AbstractUser):
    """User model extending Django's AbstractUser."""
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')

    def __str__(self):
        return str(self.username)

class Category(models.Model):
    """Category model for product categories."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    """Product model representing items for sale."""
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    brand = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='product_images/', null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((300, 300))
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            self.image = ContentFile(output.read(), name=f"{self.name}.jpg")
        super().save(*args, **kwargs)

class Wallet(models.Model):
    """Wallet model for user balance."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet" if self.user else "Wallet"

class Transaction(models.Model):
    """Transaction model for wallet operations."""
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1000000)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.wallet and self.wallet.user:
            return f"Transaction of {self.amount} for {self.wallet.user.username}"
        return "Transaction"

class CartItem(models.Model):
    """CartItem model representing items in a user's cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}" if self.product else "Cart Item"

    def total_price(self):
        """Calculate and return the total price for this cart item."""
        return self.quantity * self.product.price if self.product else 0

class Order(models.Model):
    """Order model representing a user's purchase."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.pk} by {self.user.username}" if self.user else "Order"
