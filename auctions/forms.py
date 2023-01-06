from django import forms
from .models import Category

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=128, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'autofocus': 'autofocues',
        'class': "form-control my-3"
        }))
    description = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': 'description',
        'class': "form-control",
        }))
    image_url = forms.CharField(label='', max_length=512, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Image URL',
        'class': "form-control my-3",
        }))
    price = forms.DecimalField(label='', min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Price',
        'class': "form-control my-3",
        }))
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label=None)
