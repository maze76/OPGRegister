from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Product category"


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=100, verbose_name="Ime proizvoda:")
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, 
                        null=True, verbose_name="Kategorija proizvoda:")

    def __str__(self):
        return f"{self.product_name}"
    
    class Meta:
        verbose_name_plural = "Products"


phone_regex = RegexValidator(regex=r'^\+?1?\d{7,17}$')

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    company_name = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"