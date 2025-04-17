from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from . import servises
from threading import Thread
processing_results = {}
def render_main_menu(request):
    """
    Главная страница с меню.
    """
    return render(request, 'analiticts.html')

def table_menu(request):
    return render(request, 'table.html')

def models_menu(request):
    return render(request, 'process_data.html')


def process_whatsapp(request):
    if request.method == 'POST':
        whatsapp_chat_name = request.POST.get('whatsapp_chat_name')
        # Здесь можно добавить логику обработки данных из WhatsApp
        print(f"Processing chat '{whatsapp_chat_name}' from WhatsApp")
        # После обработки перенаправляем на страницу с таблицей
        return redirect('table')  # Перенаправляем на страницу с таблицей

    return HttpResponse("Invalid request")


def process_telegram(request):
    if request.method == 'POST':
        telegram_messages = request.POST.get('telegram_messages')
        grouped_records = servises.date_model(telegram_messages)
    
        return render(request, 'table.html', {'grouped_records': grouped_records})
