from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Hair Oil')

    def __str__(self):
        return self.name



class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_slug = AutoSlugField(populate_from='product_name', unique=True, null=True, default=None) # Add this
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = HTMLField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    hot_sale = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.product_name)  # Auto-generate slug if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', blank=True, null=True)
    image_url = models.URLField('Image URL', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"

    def clean(self):
        super().clean()
        if self.image and self.image_url:
            raise ValidationError("Provide either an uploaded image or an image URL, not both.")
        if not self.image and not self.image_url:
            raise ValidationError("You must provide either an uploaded image or an image URL.")

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.discount_value} off on {self.product.product_name}"


class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Voucher: {self.code}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.product_name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
   
    quantity = models.IntegerField(default=1)
    phoneno1 = models.CharField(max_length=15)
    phoneno2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    email = models.EmailField(max_length=50, null=True, default=None)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"


class Analytics(models.Model):
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_users = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics as of {self.last_updated}"