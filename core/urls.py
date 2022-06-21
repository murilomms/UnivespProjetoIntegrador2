from django.urls import path

from .views import list_question, create_question, update_question, delete_question, list_theme, create_theme, delete_theme, update_theme

app_name = "core"

urlpatterns = [
    path('', list_question, name='list_question'),
    path('new', create_question, name='create_question'),
    path('update/<int:id>/', update_question, name='update_question'),
    path('delete/<int:id>/', delete_question, name='delete_question'),
    path('theme', list_theme, name='list_theme'),
    path('newTheme', create_theme, name='create_theme'),
    path('updateTheme/<int:id>/', update_theme, name='update_theme'),
    path('deleteTheme/<int:id>/', delete_theme, name='delete_theme'),
]