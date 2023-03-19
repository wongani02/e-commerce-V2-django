from django import forms


class NoAuthCheckoutForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': '', 'placeholder':'eg Wongani'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': '', 'placeholder':'eg Tembo'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': '', 'placeholder':'eg doe@gmail.com'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': '', 'placeholder':'eg 088223****'}),
        max_length=10,
    )
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': '','placeholder':'eg Tech IQ'}),
        required=False
    )
    district_or_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': '','placeholder':'eg Lilongwe'})
    )
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': ' mb-4', 'placeholder':'Street name '})
    )
    other_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': '', 'placeholder':'House number'}),
        required=False
    )
    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'eg leave at the door', 'rows':2}),
        required=False
    )

