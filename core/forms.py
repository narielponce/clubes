from django import forms

class GenerateFeesForm(forms.Form):
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
