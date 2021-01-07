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
    category = models.CharField(max_length = 100, )
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

    # Adding a field to reference the regular address
    regular_address = models.ForeignKey('RegularAddress', on_delete=models.SET_NULL, blank=True, null= True)

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
        return total

class DeliveryOption(models.Model):
    name = models.CharField(max_length=100)


class RegularAddress(models.Model):
    user                   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, )
    home_address           = models.CharField(max_length=100)
    apartment_address      = models.CharField(max_length=100)
    district               = models.CharField(max_length=100)
    
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
    code = models.CharField(max_length = 15)

    def __str__(self):
        return self.code


# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name','last_name','address','phone','city','country']






# class Product(models.Model):
#     name = models.CharField(max_length=255) 
#     image = models.ImageField(upload_to='product_pics') 
#     price = models.FloatField()







# from django.db import models
# from django.utils.safestring import mark_safe
# from ckeditor_uploader.fields import RichTextUploadingField
# from django.forms import ModelForm, TextInput, Textarea

# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.db.models import Avg, Count, Q, F
# # Create your models here.

# class Banner(models.Model):
#     name = models.CharField(max_length=30)
#     image = models.ImageField(blank=True,upload_to='banners/')
    
#     def __str__(self):
#         return self.name
# class Category(models.Model):
#     STATUS = (
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#     title = models.CharField(max_length=30)
#     keywords = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     image = models.ImageField(blank=True,upload_to='images/')
#     status = models.CharField(max_length=10, choices=STATUS)
    
#     slug = models.SlugField(null=False, unique=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.title 
    
#     # class MPTTMeta:
#     #     order_insertion_by = ['title']
        
#     def get_absolute_url(self):
#         return reverse("category_detail", kwargs={"slug": self.slug})
    
#     # def __str__(self):                           # __str__ method elaborated later in
#     #     full_path = [self.title]                  # post.  use __unicode__ in place of
#     #     k = "shop"
#     #     while k is not None:
#     #         full_path.append(k.title)
#     #         k = k.parent
#     #     return ' / '.join(full_path[::-1])

# class SubCategory(models.Model):
#     STATUS = (
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#     category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=30)
#     image = models.ImageField(blank=True,upload_to='images/')
#     status = models.CharField(max_length=10, choices=STATUS)
    
#     slug = models.SlugField(null=False, unique=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.title 
        
#     def get_absolute_url(self):
#         return reverse("subcategory_detail", kwargs={"slug": self.slug})
 
# class Product(models.Model):
#     STATUS = (
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#     VARIANTS = (
#         ('None', 'None'),
#         ('Size', 'Size'),
#         ('Color', 'Color'),
#         ('Size-Color', 'Size-Color'),
#     )
#     category = models.ForeignKey(Category,on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=30)
#     keywords = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     image = models.ImageField(blank=True, upload_to='images/')
#     image2 = models.ImageField(blank=True, upload_to='images/')
#     price = models.FloatField()
#     stockcount = models.IntegerField()
#     minstockcount = models.IntegerField()
#     variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
#     details = RichTextUploadingField()
#     slug = models.SlugField(null=False, unique=True)
#     status = models.CharField(max_length=10, choices=STATUS)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.title  
    
#     def get_absolute_url(self):
#         return reverse("product_detail", kwargs={"slug": self.slug})
    
#     def image_tag(self):
#         return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    
#     image_tag.short_description = 'Image'
    
#     def averagereview(self):
#         reviews = Comment.objects.filter(product=self, status="True").aggregate(average=Avg('rate'))
#         avg = 0
#         if reviews["average"] is not None:
#             avg = float(reviews["average"])
#         return avg
    
#     def countreview(self):
#         reviews = Comment.objects.filter(product=self,status="True").aggregate(count=Count('id'))
#         cnt = 0
#         if reviews["count"] is not None:
#             cnt = int(reviews["count"])
#         return cnt

# class Color(models.Model):
#     name = models.CharField(max_length=20)
#     code = models.CharField(max_length=10, blank=True,null=True)
#     def __str__(self):
#         return self.name
#     def color_tag(self):
#         if self.code is not None:
#             return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
#         else:
#             return ""

# class Size(models.Model):
#     name = models.CharField(max_length=20)
#     code = models.CharField(max_length=10, blank=True,null=True)
#     def __str__(self):
#         return self.name
# class Variants(models.Model):
#     title = models.CharField(max_length=50, blank=True,null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
#     image_id = models.IntegerField(blank=True,null=True,default=0)
#     quantity = models.IntegerField(default=10)
#     price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

#     def __str__(self):
#         return self.title

#     def thesize(self):
#         return self.size
    
#     def thecolor(self):
#         return self.color
#     def vrcost(self):
#         return self.price
    
#     def image(self):
#         img = Images.objects.get(id=self.image_id)
#         if img.id is not None:
#              varimage=img.image.url
#         else:
#             varimage=""
#         return varimage

#     def image_tag(self):
#         img = Images.objects.get(id=self.image_id)
#         if img.id is not None:
#              return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
#         else:
#             return ""
    
# class Images(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50,blank=True)
#     image = models.ImageField(blank=True)
    
#     def __str__(self):
#         return self.title

# class Setting(models.Model):
#     STATUS = (
#         ('True','True'),
#         ('False','False'),
#     )
#     title = models.CharField(max_length=150)
#     keywords = models.CharField(max_length=255)
#     description = models.CharField(blank=True, max_length=255)
#     company = models.CharField(max_length=55)
#     address = models.CharField(max_length=255)
#     phone = models.CharField(blank=True, max_length=15)
#     fax = models.CharField(blank=True, max_length=15)
#     email = models.CharField(blank=True, max_length=50)
#     smtpserver = models.CharField(blank=True, max_length=25)
#     smtpemail = models.CharField(blank=True, max_length=25)
#     smtppassword = models.CharField(blank=True, max_length=15)
#     smtpport = models.CharField(blank=True, max_length=5)
#     icon = models.ImageField(blank=True)
#     facebook = models.CharField(blank=True, max_length=50)
#     instagram = models.CharField(blank=True, max_length=50)
#     twitter = models.CharField(blank=True, max_length=50)
#     aboutus = RichTextUploadingField(blank=True)
#     contact = RichTextUploadingField(blank=True)
#     references = RichTextUploadingField(blank=True)
#     status = models.CharField(choices=STATUS, max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.title
    
# class ContactMessage(models.Model):
#     STATUS = (
#         ('New','New'),
#         ('Read','Read'),
#         ('Closed','Closed'),
#     )
#     name = models.CharField(blank=True, max_length=25)
#     email = models.CharField(blank=True, max_length=25)
#     subject = models.CharField(blank=True, max_length=50)
#     message = models.CharField(blank=True, max_length=255)
#     status = models.CharField(default='New',choices=STATUS, max_length=25)
#     ip = models.CharField(blank=True, max_length=25)
#     note = models.CharField(blank=True, max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name
    
# class ContactForm(ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['name', 'email', 'subject','message']
#         widgets = {
#             'name'   : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
#             'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
#             'email'   : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
#             'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
#         }

# class Comment(models.Model):
#     STATUS = (
#         ('New','New'),
#         ('True','True'),
#         ('False','False'),
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=250,blank=True)
#     comment = models.CharField(max_length=250, blank=True)
#     rate = models.IntegerField(default=1)
#     ip = models.CharField(max_length=20,blank=True)
#     status = models.CharField(max_length=10,choices=STATUS, default="New")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.subject
    
# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['subject', 'comment', 'rate']
        
# class ShopCart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
#     variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True)
#     quantity = models.IntegerField()
    
#     def __str__(self):
#         return self.product.title
    
#     @property
#     def price(self):
#         return (self.product.price)
    
#     @property
#     def cost(self):
#         return (self.quantity * self.product.price)
    
#     @property
#     def varcost(self):
#         return (self.quantity * self.variant.price)
# class ShopCartForm(ModelForm):
#     class Meta:
#         model = ShopCart
#         fields = ['quantity']
    
# class Order(models.Model):
#     STATUS = (
#         ('New','New'),
#         ('Accepted','Accepted'),
#         ('Preparing','Preparing')
#         ,('OnShipping','OnShipping'),
#         ('Completed','Completed'),
#         ('Canceled','Canceled'),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
#     code = models.CharField(max_length=5, editable=False)
#     first_name = models.CharField(max_length=10)
#     last_name = models.CharField(max_length=18)
#     phone = models.CharField(blank=True, max_length=20)
#     address = models.CharField(blank=True,max_length=150)
#     city = models.CharField(blank=True,max_length=20)
#     country = models.CharField(blank=True,max_length=20)
#     total = models.FloatField()
#     status = models.CharField(max_length=10,choices=STATUS, default="New")
#     ip = models.CharField(blank=True,max_length=20)
#     adminnote = models.CharField(blank=True, max_length=180)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.user.first_name
    
# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name','last_name','address','phone','city','country']

# class OrderProduct(models.Model):
#     STATUS = (
#         ('New', 'New'),
#         ('Accepted', 'Accepted'),
#         ('Canceled', 'Canceled'),
#     )
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with variant
#     quantity = models.IntegerField()
#     price = models.FloatField()
#     totalcost = models.FloatField()
#     status = models.CharField(max_length=10, choices=STATUS, default='New')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user.first_name
    
#     @property
#     def vsize(self):
#         sizer = self.variant.thesize
#         return sizer
    
#     @property
#     def vcolor(self):
#         colorr = self.variant.thecolor
#         return colorr
    
#     @property
#     def vrcost(self):
#         total = 0
#         if self.variant == 'None':
#             total += self.price * self.quantity
#         else:
#             total += self.variant.price * self.quantity
#         return total
    
# class FAQ(models.Model):
#     STATUS = (
#         ('True', 'True'),
#         ('False', 'False'),
#     )\
#     ordernumber = models.IntegerField()
#     question = models.CharField(max_length=200)
#     answer = RichTextUploadingField()
#     status=models.CharField(max_length=10, choices=STATUS)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.question
