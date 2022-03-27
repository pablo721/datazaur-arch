from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('dash/', views.DashboardView.as_view(), name='dash'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('twitter/', views.TwitterView.as_view(), name='twitter'),
    path('websites/', views.websites, name='websites'),
    path('crypto/', views.CryptoNewsView.as_view(), name='crypto_news'),
    path('events/', views.CryptoEventsView.as_view(), name='crypto_events'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    ]
