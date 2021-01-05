from django.db import models
from django.contrib.auth.models import User, auth 
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.

class WelcomeItem(models.Model):
    image                  = models.ImageField(upload_to='pics')
    description            = models.BooleanField(default=False)      # I have to design this 
    readmorebutton         = models.BooleanField(default=False)

class Item (models.Model): 
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='product_pics', blank=True, null=True) 
    price = models.FloatField()
    slug = models.SlugField()
   

     
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug}) # product_detail is the name of the url to the product.html page
    
    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})
    
    def get_remove_from_cart(self):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})

class OrderItem(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered      = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()
        
class Order(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, )
    items        = models.ManyToManyField(OrderItem)
    start_date   = models.DateTimeField(auto_now_add=True, )
    ordered_date = models.DateTimeField()
    ordered      = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total










# class Product(models.Model):
#     name = models.CharField(max_length=255) 
#     image = models.ImageField(upload_to='product_pics') 
#     price = models.FloatField()







