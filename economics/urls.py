from django.urls import path

from . import views

app_name = 'economics'
urlpatterns = [
    path('macro/', views.MacroView.as_view(), name='macro'),
    path('fundamentals/', views.FundamentalsView.as_view(), name='fundamentals'),
    ]