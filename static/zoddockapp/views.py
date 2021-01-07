from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import WelcomeItem, Item, OrderItem, Order, DeliveryOption, RegularAddress, Payment, Coupon
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.generic import ListView,DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, CouponForm
from django.db.models import Q # new



import stripe
#stripe.api_key = settings.STRIPE_SECRET_KEY





class HomeView(ListView):  # This lists the items
    model          = Item
    context_object_name = 'item_list'
    template_name  = "women_jeans_page.html"
    if Item.objects.all().filter(category="menshoes"):
        context_object_name = 'item_list'
        template_name  = "mens_shoes_page.html"

class ItemDetailView(DetailView):
    model               = Item
    context_object_name = 'item' # new
    template_name        = "product_detail.html"

def Menshoes(request):
    menshoes = Item.objects.all().filter(category="menshoes")
    context = {"menshoes":Item}
    print(menshoes)
   # template_name  = "mens_shoes_page.html"
    return render(request, 'mens_shoes_page.html', context)

def home_page(request):
    welcomeitems = WelcomeItem.objects.all()
    context      = {'welcomeitems':welcomeitems}
    return render(request, 'home_page.html', context)

@login_required
def add_to_cart(request, slug):                                               # slug of the item
    item                     = get_object_or_404(Item, slug=slug)   
    order_item,created       = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)                       # if there is an order, the quantity of the item will be modified
    order_qs                 = Order.objects.filter(user=request.user, ordered=False) # This ensures that we get orders wc are not completed
    if order_qs.exists():
        order = order_qs[0]   # if it exist grap the item from the  queryset
        #Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item  quantity was Updated")
            return redirect ("order-summary")
        else:
            messages.info(request, "This Item was added to your cart")
            order.items.add(order_item)
            return redirect ("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This was added to your cart")
    return redirect( "order-summary")

@login_required
def remove_from_cart(request, slug):
    item                     = get_object_or_404(Item, slug=slug) 
    order_qs                 = Order.objects.filter(user=request.user, ordered=False) # This ensures that we get orders wc are not completed
    if order_qs.exists():
        order = order_qs[0]   # if it exist grap the item from the  queryset
        #Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was aremoved from your cart")
            return redirect("order-summary")
        else:
            # add a message saying the user does not have an order
            messages.info(request, "This witem was not in your cart")
            return redirect("product_detail", slug=slug)
    else:
        messages.info(request, "You do not have an activ order")
        return redirect("product_detail", slug=slug)
    return redirect("product_detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item                     = get_object_or_404(Item, slug=slug) 
    order_qs                 = Order.objects.filter(user=request.user, ordered=False) # This ensures that we get orders wc are not completed
    if order_qs.exists():
        order = order_qs[0]   # if it exist grap the item from the  queryset
        #Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item was removed from the cart")
            return redirect("order-summary")
        else:
            # add a message saying the user does not have an order
            messages.info(request, "This witem was not in your cart")
            return redirect("product_detail", slug=slug)
    else:
        messages.info(request, "You do not have an activ order")
        return redirect("product_detail", slug=slug)
    return redirect("product_detail", slug=slug)

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object':order}
            return render(self.request, 'cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("cart.html")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        # Next we shall need to get our form and pass it into the 
        # Deliveryoption       = DeliveryOption.objects.all()
        try:
            order                 = Order.objects.get(user=self.request.user, ordered=False) # This ensures that we get orders wc are not completed
            # Next step is assigning the coupon to the order
           
            form    = CheckoutForm()
            context = {'form':form, 'order':order, 'couponform':CouponForm(), }
            return render(self.request, 'check_out.html', context)

        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active Order")
            return redirect("check_out")   # If order does not exist we redirect back to the order summary
        
    def post(self, *args, **kwargs): # This will dels withe post request of the form    
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid(): # Then the next step grabs all the data from the  the posted form  
                home_address        = form.cleaned_data.get('home_address')
                apartment_address   = form.cleaned_data.get('apartment_address')
                district            = form.cleaned_data.get('district')
                phone_number        = form.cleaned_data.get('phone_number')
                # address_choice      = form.cleaned_data.get('address_choice')
                # save_info           = form.cleaned_data.get('save_info')
                payment_option      = form.cleaned_data.get('payment_option')
                delivery_choice     = form.cleaned_data.get('delivery_choice')

                regular_address = RegularAddress(
                    user = self.request.user,
                    home_address           = home_address,
                    apartment_address      = apartment_address,
                    district               = district, 

                )
                regular_adress.save()
                order.regular_address = regular_address
                order.save()

                if payment_option == 'Stripe':
                    return redirect('payment', payment_option = 'Stripe')  # Put the name of the url of payment
                elif paymet_option == 'Flutter Wave':
                    return redirect('payment', payment_option = 'Flutter Wave')  # Put the name of the url of payment
                else:
                    messages.warning(self.request, "Invalid Payment Option")
                    return redirect('check_out')
            
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order-summary")

        
        if form.is_valid(): # Then the next step grabs all the data from the  the posted form  
            home_address        = form.cleaned_data.get('home_address')
            apartment_address   = form.cleaned_data.get('apartment_address')
            district            = form.cleaned_data.get('district')
            phone_number        = form.cleaned_data.get('phone_number')
            address_choice      = form.cleaned_data.get('address_choice')
            save_info           = form.cleaned_data.get('save_info')
            payment_option      = form.cleaned_data.get('payment_option')
            delivery_choice     = form.cleaned_data.get('delivery_choice')

            regular_address = RegularAddress(
                user = self.request.user,
                home_address           = home_address,
                apartment_address      = apartment_address,
                district               = district, 

            )

class PaymentView(View):
    def get(self, *args, **kwargs):
        # order ie we shall pass the order in the context
        return render(self.request, "payment.html")  

    def post(self, *arg, **kwarg):                       #  Receiving the token fron Stripe
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        charge = stripe.charge.create(
            amount = amount,  # * by 100 becoz the value is in cents
            currency = "usd",
            source = token,
            description = "Charge"
            )      
        
        # Creating the  Payment
        payment                  = Payment()
        payment.stripe_charge_id = charge['id']
        payment.user             =  self.request.user
        payment.amount           =  order.get_total() 
        payment.save()

        # Assisgning the payment to ther order

        order_items  = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:          # Loop through every order item in order.items.all() queryset and save each order item
            item.save()

        order.ordered = True
        order.payment = payment
        order.save()

def  get_coupon(request, code): 
    try:
        coupon                = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exit")
        return redirect("check_out")   
    



def add_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order                 = Order.objects.get(user=request.user, ordered=False) # This ensures that we get orders wc are not completed
                # Next step is assigning the coupon to the order
                order.coupon                = get_coupon(request, code)
                order.save()
                messages.success(request, "Successfully added coupon")
                return redirect("check_out")   


            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active Order")
                return redirect("check_out")   # If order does not exist we redirect back to the order summary
    # Todo raise error
    return None
            




# @login_required(login_url="/users/login")
# def cart_add(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     order_item, = OrderItem.objects.get_or_create(item=product ) #
#     cart.add(product=product)

#     return redirect("cart")


# @login_required(login_url="/users/login")
# def item_clear(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.remove(product)
#     return redirect("cart_detail")


# @login_required(login_url="/users/login")
# def item_increment(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("cart")


# @login_required(login_url="/users/login")
# def item_decrement(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.decrement(product=product)
#     return redirect("cart")


# @login_required(login_url="/users/login")
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")


# @login_required(login_url="/users/login")
# def cart_detail(request):
#     return render(request, 'cart/cart_detail.html')
# # In the template you can use the url in folowing way:

# @login_required(login_url="/users/login")
# def cart(request):
#     return render(request,'cart.html')
   

# def women_jeans_page(request):
#     products = Product.objects.all()
#     context  = {'products': products}
#     return render (request, 'women_jeans_page.html',context)
# def check_out(request):
#     return render(request, 'check_out.html')

    
