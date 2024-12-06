# main/models.py
from django.db import models

class Request(models.Model):
    VEHICLE_CHOICES = [
        ('sedan', 'Седан'),
        ('suv', 'Внедорожник'),
        ('special', 'Спецтехника'),
    ]

    pickup_location = models.CharField("Адреса", max_length=255, blank=True, null=True)
    dropoff_location = models.CharField("Куда доставить", max_length=255, blank=True, null=True)
    vehicle_info = models.CharField("Что перевезти?", max_length=50, choices=VEHICLE_CHOICES, blank=True, null=True)
    wheels_blocked = models.PositiveIntegerField("Количество заблокированных колес", default=0, blank=True, null=True)
    steering_blocked = models.BooleanField("Руль заблокирован?", default=False, blank=True, null=True)
    additional_comments = models.TextField("Дополнительный комментарий", blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=20)  # обязательное поле, без blank=True/null=True
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.id}"
    
class ContactRequest(models.Model):
    name = models.CharField("Имя", max_length=100, blank=True, null=True)  # Поле для имени
    phone_number = models.CharField("Номер телефона", max_length=20)  # Обязательное поле для номера телефона
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)  # Автоматическая отметка времени

    def __str__(self):
        return f"Контакт #{self.id} - {self.phone_number} ({self.name or 'Без имени'})"
