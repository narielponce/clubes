from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 
                 'fecha_nacimiento', 'dni', 'contacto_emergencia', 'telefono_emergencia')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove password field from edit form
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'direccion', 
                 'fecha_nacimiento', 'dni', 'contacto_emergencia', 'telefono_emergencia')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
