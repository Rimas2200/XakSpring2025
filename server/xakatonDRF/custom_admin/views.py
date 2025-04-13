
from django.shortcuts import render

def custom_menu_view(request):
    return render(request, 'admin/custom_menu.html', {
        'title': 'Управлени сообщениями',
        'side_menu': [
                {'label': 'Подменю 1', 'url': '/admin/custom-menu/submenu-1/'},
                {'label': 'Подменю 2', 'url': '/admin/custom-menu/submenu-2/'},
            ]
        })


def submenu_1_view(request):
    return render(request, 'admin/submenu_1.html', {'title': 'Подменю 1'})

def submenu_2_view(request):
    return render(request, 'admin/submenu_2.html', {'title': 'Подменю 2'})