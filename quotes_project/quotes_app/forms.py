from django import forms
from .models import Author, Quote


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'
