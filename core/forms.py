from django import forms

class GenerateFeesForm(forms.Form):
    description = forms.CharField(
        label="Descripción de la Cuota",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ej: Cuota Mensual Octubre'})
    )
    amount = forms.DecimalField(
        label="Monto",
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'input', 'step': '0.01'})
    )
    period = forms.DateField(
        label="Período (selecciona cualquier día del mes correspondiente)",
        required=True,
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'})
    )
    due_date = forms.DateField(
        label="Fecha de Vencimiento",
        required=True,
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'})
    )
