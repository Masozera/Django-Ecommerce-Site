from django.db import models
from django.contrib.auth.models import User, auth 
from django.shortcuts import reverse
from django.conf import settings

''' 
1.Item added to the cart
2.Adding billing address
3.Payment
(Preprocessing, Processing, Packaging)
4.Being Delivered
5.Received
6. Refunds
'''

# Create your models here.

class WelcomeItem(models.Model):
    image                  = models.ImageField(upload_to='pics')
    description            = models.BooleanField(default=False)      # I have to design this 
    readmorebutton         = models.BooleanField(default=False)

class Item (models.Model): 
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='product_pics', blank=True, null=True) 
    price = models.FloatField()
    category = models.CharField(max_length = 100, blank=True, null=True)
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
    ref_code     = models.CharField(max_length=20)
    items        = models.ManyToManyField(OrderItem)
    start_date   = models.DateTimeField(auto_now_add=True, )
    ordered_date = models.DateTimeField()
    ordered      = models.BooleanField(default=False)

    being_delivered      = models.BooleanField(default=False)
    received             = models.BooleanField(default=False)
    refund_requested     = models.BooleanField(default=False)
    refund_granted       = models.BooleanField(default=False)

    # Adding a field to reference the billing address
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null= True)

     # Adding a field to reference the Payment
    payment         = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null= True)

    # Adding a field to reference the Coupon
    coupon         = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null= True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        total -= self.coupon.amount
        return total

class DeliveryOption(models.Model):
    name = models.CharField(max_length=100)


class BillingAddress(models.Model):
    user                   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True)
    home_address           = models.CharField(max_length=100, blank=True, null=True )
    apartment_address      = models.CharField(max_length=100,blank=True, null=True)
    district               = models.CharField(max_length=100,blank=True, null=True)
    
    def __str__(self):
        return self.user.username


class Payment(models.Model): # This keeps track of the payments
    stripe_charge_id = models.CharField(max_length= 30)
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, blank=True, null=True)  # on_delete is ete to SET_NULL so that we don't delete the payment if the user was deleted
    amount           = models.FloatField()
    timestamp        = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username

# Dicount Codes
class  Coupon(models.Model):
    code   = models.CharField(max_length = 15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason    = models.TextField()
    accepted  = models.BooleanField(default=False)
    email     = models.EmailField()

    def __str__(self):
        return f"{self.pk}" 

