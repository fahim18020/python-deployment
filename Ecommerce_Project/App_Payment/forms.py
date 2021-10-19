from django import forms
from App_Payment.models import BillingAddress
from django.views.decorators.csrf import csrf_protect

class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address','zipcode','city','country']
