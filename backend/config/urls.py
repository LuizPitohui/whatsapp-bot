from django.contrib import admin
from django.urls import path
from bot.views import WebhookView, dashboard_home  # <--- Importe aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/webhook/', WebhookView.as_view(), name='webhook'),
    
    # NOVA ROTA:
    path('dashboard/', dashboard_home, name='dashboard'),
]