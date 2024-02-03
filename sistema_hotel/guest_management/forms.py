#forms.pys

from .models import Booking, CheckOut
from django import forms



# Garantir que DateInput esteja importado
class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class BookingCheckInForm(forms.ModelForm):
    room_number = forms.CharField(max_length=10, widget=forms.HiddenInput(), required=False)  # Campo oculto para o número do quarto
    class Meta:
        model = Booking
        fields = ['full_name', 'cpf', 'email', 'phone_number', 'address',
                  'companions', 'travel_reason', 'daily_rate',
                  'number_of_days', 'check_in', 'check_out', 'room_number']
        widgets = {
            'check_in': DateInput(attrs={'class': 'form-control', 'format': '%Y-%m-%dT%H:%M'}),
            'check_out': DateInput(attrs={'class': 'form-control', 'format': '%Y-%m-%dT%H:%M'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 40, 'style': 'resize:none;'}),
            'companions': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 40, 'style': 'resize:none;'}),
            'daily_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'R$'}),
            # Adicione a classe 'form-control' aos outros campos também
        }
        labels = {
            # Adicione os rótulos conforme necessário
        }




class BookingCheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ['room_consumption', 'observations', 'payment_method', 'total_paid']
        widgets = {
            'room_consumption': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 40, 'style': 'resize:none;'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 40, 'style': 'resize:none;'}),
            'payment_method': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 40, 'style': 'resize:none;'}),
            'total_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'R$'}),
            #'closing_date': DateInput(attrs={'class': 'form-control', 'format': '%Y-%m-%dT%H:%M'}),
            # Adicione a classe 'form-control' aos outros campos também
        }
        labels = {
            # Adicione os rótulos conforme necessário
        }