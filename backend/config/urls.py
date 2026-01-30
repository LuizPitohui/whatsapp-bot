from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui as rotas do bot com o prefixo /api/
    path('api/', include('bot.urls')),
]