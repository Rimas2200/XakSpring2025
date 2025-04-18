from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from urllib.parse import unquote

import json

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


def correct_loading_date_tg(request):
    if request.method == 'POST':
        telegram_messages = request.POST.get('telegram_messages')
        grouped_records = servises.t5_processing_model_tg(int(telegram_messages))
        grouped_records_json = json.dumps(grouped_records)
        return render(request, 'intermediate_screen.html', {
            'grouped_records': grouped_records,
            'grouped_records_json': grouped_records_json,
        })
    
    # Если GET-запрос, просто показываем форму
    return render(request, 'correct_loading_date.html')

def correct_loading_date_whatsapp(request):
    if request.method == 'POST':
        whatsapp_chat_name = request.POST.get('whatsapp_chat_name')
        grouped_records = servises.t5_processing_model_whatsapp(whatsapp_chat_name)
        grouped_records_json = json.dumps(grouped_records)
        return render(request, 'intermediate_screen.html', {
            'grouped_records': grouped_records,
            'grouped_records_json': grouped_records_json,
        })
      
    # Если GET-запрос, просто показываем форму
    return render(request, 'correct_loading_date.html')

def load_data_to_table(request):
    if request.method == 'POST':
         # Собираем измененные данные из формы
        edited_records = []
        for key, value in request.POST.items():
            if key.startswith('record_'):
                # Декодируем значение, если оно URL-encoded
                decoded_value = unquote(value)
                edited_records.append(decoded_value.split('\n'))
                  # Разделяем строки обратно в список
        print(edited_records)
        grouped_records = servises.neiro_model(edited_records)
        # Передаем данные в таблицу
        return render(request, 'table.html', {'grouped_records': grouped_records})
    
    return HttpResponse("Invalid request")
