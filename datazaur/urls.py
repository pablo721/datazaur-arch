
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('markets/', include('markets.urls'), name='markets'),
    path('economics/', include('economics.urls'), name='economics'),
    path('news/', include('news.urls'), name='news'),
    #path('trade/', include('trade.urls'), name='trade'),
    path('messenger/', include('messenger.urls'), name='messenger'),
    path('', include('website.urls'), name='website'),
]

