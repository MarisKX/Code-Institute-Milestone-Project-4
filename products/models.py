from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Manufacturer(models.Model):
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

class TyreSize(models.Model):
    width = models.PositiveIntegerField(default=125, validators=[MinValueValidator(125), MaxValueValidator(345)])
    heigth = models.PositiveIntegerField(default=55, validators=[MinValueValidator(25), MaxValueValidator(80)])
    rim_size = models.PositiveIntegerField(default=16, validators=[MinValueValidator(12), MaxValueValidator(26)])
    full_size_code = models.CharField(max_length=8, null=True, blank=True)
    full_size_display = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return self.full_size_code

    def get_display_name(self):
        return self.full_size_display

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.full_size_code = str(self.width) + str(self.heigth) + "R" + str(self.rim_size)
        self.full_size_display = str(self.width) + "/" + str(self.heigth) + " R" + str(self.rim_size)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    ean = models.CharField(max_length=254, null=True, blank=True)
    size = models.ForeignKey('TyreSize', null=True, blank=True, on_delete=models.SET_NULL)
    load_index = models.CharField(max_length=254, null=True, blank=True)
    speed_index = models.CharField(max_length=254, null=True, blank=True)
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
