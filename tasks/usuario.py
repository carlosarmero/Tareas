from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms

from django.forms import ModelForm, Textarea

class Crearusuario(UserCreationForm):
    
    class Meta:
        model = User  
        fields = ['email', 'password1', 'password2']
        widgets = {'email' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'correo@email.com'})}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = 'Su contraseña debe contener al menos 6 caracteres.'
       # self.fields['password2'].help_text = 'password2 help_text'