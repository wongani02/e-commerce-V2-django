from django import forms 


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'Email Address'}
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':'What\'s this about?'}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder':'Your message....'})
    )