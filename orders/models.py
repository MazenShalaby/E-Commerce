from django.db import models
import string, random
from django.core.validators import MinValueValidator, MaxValueValidator

from inventory.models import Product

# Create your models here.


def generate_order_id(length=16):
    characters = string.ascii_letters + string.digits # str
    random_characters = random.choices(characters, k=length) # list 
    return "".join(random_characters) # str

class Order(models.Model):
    class EgyptGovernorates(models.TextChoices):
        CAIRO = "Cairo", "Cairo"
        GIZA = "Giza", "Giza"
        ALEXANDRIA = "Alexandria", "Alexandria"
        DAKAHLIA = "Dakahlia", "Dakahlia"
        RED_SEA = "Red Sea", "Red Sea"
        BEHEIRA = "Beheira", "Beheira"
        FAYOUM = "Fayoum", "Fayoum"
        GHARBIA = "Gharbia", "Gharbia"
        ISMAILIA = "Ismailia", "Ismailia"
        MENOFIA = "Menofia", "Menofia"
        MINYA = "Minya", "Minya"
        QALYUBIA = "Qalyubia", "Qalyubia"
        NEW_VALLEY = "New Valley", "New Valley"
        SUEZ = "Suez", "Suez"
        ASWAN = "Aswan", "Aswan"
        ASSIUT = "Assiut", "Assiut"
        BENI_SUEF = "Beni Suef", "Beni Suef"
        PORT_SAID = "Port Said", "Port Said"
        DAMIETTA = "Damietta", "Damietta"
        SHARKIA = "Sharkia", "Sharkia"
        SOUTH_SINAI = "South Sinai", "South Sinai"
        KAFR_EL_SHEIKH = "Kafr El Sheikh", "Kafr El Sheikh"
        MATROUH = "Matrouh", "Matrouh"
        LUXOR = "Luxor", "Luxor"
        QENA = "Qena", "Qena"
        NORTH_SINAI = "North Sinai", "North Sinai"
        SOHAG = "Sohag", "Sohag"
    order_id = models.CharField(max_length=16, unique=True, default=generate_order_id)
    email = models.EmailField()
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    state_governorates = models.CharField(max_length=50, choices=EgyptGovernorates.choices, null=True)
    city = models.CharField(max_length=30)
    postal_code = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            unique_order_id = generate_order_id()
            while Order.objects.filter(order_id__iexact=unique_order_id).exists():
                unique_order_id = generate_order_id()
            self.order_id = unique_order_id
        super().save(*args, **kwargs) # Call the real save() method
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['paid']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Order ID: {self.order_id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
