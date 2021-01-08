from django import template
from zoddockapp.models import Order

register = template.Library()       # This enables us register our template tag

@register.filter
def cart_item_count(user):          # This will be the name of the template tag
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()   # qs[0] is getting thr only order in that queryset, items.count is getting the count of the items in the order
    return 0                              # If the user is not authenticated return 0