from django import forms


class AnonymousOrderSearchForm(forms.Form):
    order_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'name':'order_email', 'placeholder':'Email you used during checkout'}),
        required=True
    )
    order_key = forms.CharField(
        widget=forms.TextInput(attrs={'name': 'order_key ', 'placeholder':'Found in your order confirmation email.'})
    )