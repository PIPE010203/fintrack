from django import forms
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['categoria', 'limite', 'mes', 'anio']
        widgets = {
            'mes': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'anio': forms.NumberInput(attrs={'min': 2024, 'max': 2030}),
        }