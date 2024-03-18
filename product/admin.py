from django.contrib import admin
from .models import *

class PSPInline(admin.StackedInline):
    model = ProductSizePrice
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [PSPInline]
    
class OIInline(admin.StackedInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OIInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizePrice)
admin.site.register(Group)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Info)
admin.site.register(Banner)