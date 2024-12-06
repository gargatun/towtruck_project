from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RequestForm, ContactForm
from .models import Request, ContactRequest
import requests

# Главная страница
def home(request):
    # Сначала инициализируем формы
    form = RequestForm()
    contact_form = ContactForm()

    if request.method == 'POST' and 'request-form' in request.POST:
        # Обработка формы "Оставить заявку"
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save()
            send_telegram_notification(new_request)
            return redirect('success')
    elif request.method == 'POST' and 'contact-form' in request.POST:
        # Обработка контактной формы
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_request = contact_form.save()
            send_telegram_contact_notification(contact_request)
            return redirect('success')

    context = {
        'form': form,
        'contact_form': contact_form,
        'geocode_api_key': settings.YANDEX_GEOCODE_API_KEY,
        'static_map_api_key': settings.YANDEX_STATIC_MAP_API_KEY,
        'suggest_api_key': settings.YANDEX_SUGGEST_API_KEY,
    }
    return render(request, 'main/home.html', context)

# Страница успеха
def success(request):
    return render(request, 'main/success.html')

# Уведомление в Telegram для формы "Оставить заявку"
def send_telegram_notification(request_obj):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)

    if not token or not chat_id:
        return

    message_text = (
        f"Новая заявка #{request_obj.id}\n"
        f"Откуда забрать: {request_obj.pickup_location or 'Не указано'}\n"
        f"Куда доставить: {request_obj.dropoff_location or 'Не указано'}\n"
        f"Транспорт: {request_obj.get_vehicle_info_display() if request_obj.vehicle_info else 'Не указан'}\n"
        f"Заблокированных колес: {request_obj.wheels_blocked}\n"
        f"Руль заблокирован: {'Да' if request_obj.steering_blocked else 'Нет'}\n"
        f"Доп. комментарии: {request_obj.additional_comments or 'Нет'}\n"
        f"Телефон: {request_obj.phone_number}\n"
        f"Дата/время: {request_obj.created_at.strftime('%Y-%m-%d %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

# Уведомление в Telegram для формы "Связаться с нами"
def send_telegram_contact_notification(contact_request):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)

    if not token or not chat_id:
        return

    message_text = (
        f"Новая заявка на связь:\n"
        f"Имя: {contact_request.name}\n"
        f"Телефон: {contact_request.phone_number}\n"
        f"Дата/время: {contact_request.created_at.strftime('%Y-%m-%d %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
