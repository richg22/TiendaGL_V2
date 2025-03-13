from django import forms
from .models import Producto, Cliente

class MiFormulario(forms.ModelForm):
    class Meta:
        model = Producto
        exclude=['id']

class ClienteCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Cliente
        fields = ('email', 'nombre', 'rut', 'direccion')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data["password"])
        if commit:
            cliente.save()
        return cliente
    
class LoginForm(forms.Form):
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
