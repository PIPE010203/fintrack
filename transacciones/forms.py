from django import forms
from .models import Gasto, Ingreso

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descripcion', 'monto', 'categoria', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej: Almuerzo en la U'}),
            'monto': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['descripcion', 'monto', 'categoria', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej: Salario mensual'}),
            'monto': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }