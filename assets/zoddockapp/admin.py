from django.contrib import admin
from .models import WelcomeItem,Item, OrderItem, Order,BillingAddress, DeliveryOption, Payment, Coupon, Refund

def make_refund_accepted(modeladmin, request, queryset):  # This eilll udate the status of the request refund to granted
    queryset.update(refund_requested=False, refund_granted=True )
make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received', 
                    'refund_requested',
                    'refund_granted',
                    # 'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]   # This displays the ordered order

    list_display_links = [
        'user',
        #'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    search_fields = [
        'user__username',
        'ref_code'
    ]

    list_filter = ['ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted']
    actions =[make_refund_accepted]

# class AddressAdmin(admin.ModelAdmin):
#     list_display = [
#             'user'       
#             'address'    
#             'zip'        
#             'country'    
#             'district'   
#             'address_type' 
#             'default'   
#         ]
#     list_filter     = ['country', 'default', 'address_type',]
#     search_fields   = ['user', 'address', 'zip', 'country', 'district', 'address_type',  'default']
# Register your models here.
admin.site.register(WelcomeItem),
admin.site.register(Item),
admin.site.register(OrderItem),
admin.site.register(Order, OrderAdmin),
admin.site.register(DeliveryOption),
admin.site.register(Payment),
admin.site.register(Coupon),
admin.site.register(BillingAddress),
# admin.site.register(OrderItem),
# admin.site.register(Order,OrderAdmin),
# admin.site.register(Payment),
# admin.site.register(Coupon),
# admin.site.register(Refund),
# admin.site.register(Address,AddressAdmin),


