from django import forms

PAYMENT_CHOICES=(   
    ('Flutter Wave','Flutter Wave'),
    ('Stripe','Stripe'),
    ('Cash', 'Cash On Delivery')
)

save_info=(
    ('save info','Save Info'),
     ('','')
)

shipping_charge=(
    ('Standard','Free')
)

address_choices = (
    ('Regular_Adress', 'Use my regular address'),
    ('Different_Address','Use a different address')
)

delivery_choices = (
    
    ('standard','UGX 10,000'),
)


class CheckoutForm(forms.Form):
    home_address         = forms.CharField (widget=forms.TextInput(attrs={'placeholder':'Home address'}))
    apartment_address    = forms.CharField (widget=forms.TextInput(attrs={'placeholder':'Apartment address'}))
    district             = forms.CharField (widget=forms.TextInput(attrs={'placeholder':'District'}))
    phone_number         = forms.CharField (widget=forms.TextInput(attrs={'placeholder':'Phone no.'}))
    address_choice       = forms.ChoiceField(widget=forms.RadioSelect, choices=address_choices)
    save_info            = forms.ChoiceField(widget=forms.CheckboxInput(), required=False)
    payment_option       = forms.ChoiceField(widget=forms.RadioSelect, choices = PAYMENT_CHOICES)
    delivery_choice      = forms.ChoiceField(widget=forms.CheckboxInput(),choices = delivery_choices)


class CouponForm(forms.Form):
    code = forms.CharField(widget= forms.TextInput(attrs={'placeholder': 'Enter promo code'}))
