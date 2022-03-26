from django.urls import path, include
from . import views


app_name = 'crypto'
urlpatterns = [
    path('', views.crypto, name='crypto'),
    path('exchanges/', views.ExchangesView.as_view(), name='exchanges'),
    path('addExchange/', views.add_exchange, name='add_exchange'),
    path('dominance/', views.DominanceView.as_view(), name='dominance'),
    path('global_metrics/', views.GlobalMetricsView.as_view(), name='global_metrics'),
    path('watchlist/', views.WatchlistView.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', views.WatchlistView.as_view(), name='watchlist2'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('trends/', views.TrendsView.as_view(), name='trends'),
    path('defi/', views.DeFiView.as_view(), name='defi'),
    path('nft/', views.NFTView.as_view(), name='nft'),
    path('calendar/', views.CryptoCalendarView.as_view(), name='calendar'),
    ]
