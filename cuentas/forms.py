from django import forms
from .models import Usuario
from .validators import validate_password
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
    widget=forms.PasswordInput, 
    validators=[validate_password], 
    max_length=16
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'password']
    
    # Metodo para hashear la password
    def clean_password(self):
        password = self.cleaned_data['password']
        return make_password(password)