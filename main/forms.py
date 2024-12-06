# main/forms.py

from django import forms
from .models import Request
from .models import ContactRequest

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'
        widgets = {
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Откуда забрать', 
                'id': 'id_pickup_location'
            }),
            'dropoff_location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Куда доставить', 
                'id': 'id_dropoff_location'
            }),
            'vehicle_info': forms.HiddenInput(attrs={'id': 'id_vehicle_info'}),
            'wheels_blocked': forms.HiddenInput(attrs={
                'id': 'id_wheels_blocked', 
                'value': 0
            }),
            'steering_blocked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'additional_comments': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Дополнительный комментарий'
            }),
            'phone_number': forms.HiddenInput(attrs={'id': 'id_phone_number'}),  # Заполняется через модальное окно
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone_number']  # Поля формы
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя',
                'required': False  # Имя необязательно
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
                'required': True  # Номер телефона обязателен
            }),
        }
        labels = {
            'name': 'Имя',
            'phone_number': 'Телефон'
        }
