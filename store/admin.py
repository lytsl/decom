from django.contrib import admin

from .models import Product, ProductImage


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available')
    ordering = ('category',)

    class Meta:
        model = Product


admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
