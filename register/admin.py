from django.contrib import admin
from .models import ProductCategory, Product, Company

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ("product_category",)
    list_display = ("product_name", "product_category",)

class CompanyAdmin(admin.ModelAdmin):
    list_filter = ("user", "company_name", "products",)


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Company, CompanyAdmin)
