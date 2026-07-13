from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=1500)
    image = models.ImageField(upload_to='product/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['description']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"product_slug": self.slug})

