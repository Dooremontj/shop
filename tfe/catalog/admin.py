from django.contrib import admin
from catalog.models import Supplier, Product, Order, OrderItem, Resident
from catalog.forms import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import DateWidget

class ResidentResource(resources.ModelResource):

    class meta:
        model = Resident
        widgets = {
                'birthdate': {'format': '%d/%m/%Y'},
                'datein': {'format': '%d/%m/%Y'},
                }
        
        
class ResidentAdmin(ImportExportModelAdmin):
    pass
    #resource_class = ResidentResource

admin.site.register(Resident, ResidentAdmin)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'supplier_mail', 'supplier_tel')
    pass

# Register the admin class with the associated model

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemForm
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    pass

# Register the admin class with the associated model

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    form = OrderItemForm

# @admin.register(Resident)

    
# Register the admin class with the associated model

#admin.site.register(Supplier)
#admin.site.register(Product)
#admin.site.register(Order)
#admin.site.register(OrderItem)
