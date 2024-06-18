from django import forms
from main_app.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # You can specify the fields you want to include in the form here
def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'maxlength': 50})  # Set max length and optional widget

