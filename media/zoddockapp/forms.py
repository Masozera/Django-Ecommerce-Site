from django import forms


class CheckoutForm(forms.Form):
    home_address         = forms.CharField()
    apartment_address    = forms.CharField(required=False)
    district             = forms.CharField()
    phone_number         = forms
    same_regular_address = forms.BooleanField(widget=forms.RadioSelect())
    save_info            = forms.BooleanField(widget=forms.RadioSelect())
    payment_option       = forms.BooleanField(widget=forms.RadioSelect())