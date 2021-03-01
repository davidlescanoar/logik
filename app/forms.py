from django.forms import ModelForm, Textarea
from app.models import *


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        labels = {
            'text': '',
        }
        widgets = {
            'text': Textarea(attrs={'class': 'form-control'}),
        }
