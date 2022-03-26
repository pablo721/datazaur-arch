
from django.urls import path
from . import views

app_name = 'messenger'
urlpatterns = [
    path('', views.messenger, name='messenger'),
    path('<int:friend_id>', views.chat, name='chat'),
    path('getMessages/<int:friend_id>', views.get_messages, name='getMessages'),
    path('send/', views.send, name='send')
    ]



