from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm

class ProfileUpdateForm(UserChangeForm):
    password = None  # On ne montre pas le champ password ici

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }