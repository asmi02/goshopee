from django.contrib import admin

from productshopping.forms import SizeAdminForm
from productshopping.models import Category, Sizes, Product, SubCategory, Order, Order_Details

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)

# admin.site.register(Order)
# admin.site.register(Order_Details)

admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','username','name','address','phone','order_date','order_update_date','payment_mode','grandtotal','order_status']
@admin.register(Order_Details)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['orderno','product_id','price','qty','total_cost']


class SizeAdmin(admin.ModelAdmin):
    form = SizeAdminForm

admin.site.register(Sizes, SizeAdmin)
