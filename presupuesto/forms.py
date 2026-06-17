from django import forms
from django.core.exceptions import ValidationError
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['categoria', 'limite', 'mes', 'anio']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'mes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'min': 2024, 'max': 2030}),
        }

    def clean_limite(self):
        limite = self.cleaned_data['limite']
        if limite <= 0:
            raise ValidationError('El límite debe ser mayor a cero.')
        return limite