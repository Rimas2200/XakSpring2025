
from django.shortcuts import render
from .custom_admin import custom_admin_site
from . import serives

def custom_menu_view(request):
    result = serives.date_model()
    model_data = [
        {'end': 1, 'entity': 'DATE', 'start': 0, 'text': '"28.03.25г.'},
        {'end': 3, 'entity': 'DEPARTMENT', 'start': 1, 'text': 'СП Коломейцево'},
        {'end': 5, 'entity': 'OPERATION', 'start': 3, 'text': 'предпосевная культивация'},
        {'end': 7, 'entity': 'CROP', 'start': 6, 'text': 'подсолнечник'},
        {'end': 9, 'entity': 'HECTARE', 'start': 8, 'text': '40га'},
        {'end': 11, 'entity': 'HECTARE', 'start': 11, 'text': '60га(29%)'},
        {'end': 13, 'entity': 'OPERATION', 'start': 12, 'text': 'Сев'},
        {'end': 17, 'entity': 'HECTARE', 'start': 16, 'text': '30га'},
        {'end': 19, 'entity': 'HECTARE', 'start': 19, 'text': '295га(94%)'},
        {'end': 21, 'entity': 'OPERATION', 'start': 20, 'text': 'сев'}
    ]
    print(result)  # Отладочный вывод
    return render(request, 'admin/custom_menu.html', {'records': model_data})


def submenu_1_view(request):
    return render(request, 'admin/submenu_1.html', {'title': 'Подменю 1'})

def submenu_2_view(request):
    return render(request, 'admin/submenu_2.html', {'title': 'Подменю 2'})
