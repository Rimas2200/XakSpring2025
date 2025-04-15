from django.shortcuts import render

def render_main_menu(request):
    """
    Главная страница с меню.
    """
    return render(request, 'menu.html')

def table_menu(request):
    records = [
        {'entity': 'Пример 1', 'text': 'Текст 1', 'start': 0, 'end': 1},
        {'entity': 'Пример 2', 'text': 'Текст 2', 'start': 2, 'end': 3},
    ]
    return render(request, 'table.html', {'records': records})