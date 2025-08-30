from django.contrib import admin
from .models import Product, Analytics, ProductImage, Cart, Order, Contact, Category, Discount, Voucher
from django.utils.html import format_html
from django import forms
from django.shortcuts import render
from django.urls import path
from django.db.models import Sum, Count
from django.utils.timezone import now
import datetime
import json
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.contrib.admin import AdminSite
from django.core.exceptions import ValidationError


# -----------------------------
# Custom form for Product admin
# -----------------------------
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('product_slug',)

# -----------------------------
# Custom form for ProductImage
# -----------------------------
class ProductImageAdminForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if image and image_url:
            raise forms.ValidationError("Only one of 'image' or 'image_url' should be provided.")
        if not image and not image_url:
            raise forms.ValidationError("You must provide either an uploaded image or an image URL.")
        return cleaned_data

# -----------------------------
# Category Admin
# -----------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# -----------------------------
# Product Image Inline for Product
# -----------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# -----------------------------
# Product Admin
# -----------------------------
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('product_name', 'category', 'product_price', 'stock', 'hot_sale')
    list_filter = ('category', 'hot_sale', 'stock')
    search_fields = ('product_name', 'category__name')
    inlines = [ProductImageInline]
    list_editable = ('stock', 'hot_sale')

    def product_image_preview(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.product_image.url)
        return "(No Image)"
    product_image_preview.short_description = "Image"

# -----------------------------
# ProductImage Admin
# -----------------------------
class ProductImageAdmin(admin.ModelAdmin):
    form = ProductImageAdminForm
    list_display = ['product', 'preview_image_or_url']
    search_fields = ['product__product_name']

    def preview_image_or_url(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="50" height="50" />', obj.image_url)
        return "No image"
    preview_image_or_url.short_description = "Preview"

# -----------------------------
# Discount Admin
# -----------------------------
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_type', 'discount_value', 'start_date', 'end_date')
    list_filter = ('discount_type', 'start_date', 'end_date')
    search_fields = ('product__product_name',)

# -----------------------------
# Voucher Admin
# -----------------------------
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'usage_limit')
    list_filter = ('discount_type', 'valid_from', 'valid_to')
    search_fields = ('code',)

# -----------------------------
# Cart Admin
# -----------------------------
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__product_name')

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# -----------------------------
# Order Admin
# -----------------------------
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product','quantity', 'order_date', 'total_price', 'status')
    list_filter = ('status', 'order_date', 'user', 'product')
    search_fields = ('user__username', 'product__product_name')
    list_editable = ('status',)
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

# -----------------------------
# Contact Admin
# -----------------------------
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# -----------------------------
# Analytics Admin with Dashboard
# # -----------------------------
# class AnalyticsAdmin(admin.ModelAdmin):
#     change_list_template = "admin/analytics_dashboard.html"

#     def changelist_view(self, request, extra_context=None):
#         orders_per_status = Order.objects.values("status").annotate(count=Count("id"))
#         sales_data = Order.objects.values("order_date").annotate(total_sales=Sum("total_price"))

#         status_labels = [entry["status"] for entry in orders_per_status]
#         status_values = [entry["count"] for entry in orders_per_status]

#         sales_labels = [entry["order_date"].strftime("%Y-%m-%d") for entry in sales_data]
#         sales_values = [entry["total_sales"] for entry in sales_data]

#         extra_context = extra_context or {}
#         extra_context["status_labels"] = json.dumps(status_labels)
#         extra_context["status_values"] = json.dumps(status_values)
#         extra_context["sales_labels"] = json.dumps(sales_labels)
#         extra_context["sales_values"] = json.dumps(sales_values)

#         return super().changelist_view(request, extra_context=extra_context)

# # -----------------------------
# # Admin Registration
# # -----------------------------
# admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Voucher, VoucherAdmin)


# Unregister User and Group so they don't show up at all
