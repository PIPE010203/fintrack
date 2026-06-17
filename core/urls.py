from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('dashboard/')),
    path('usuarios/', include('usuarios.urls')),
    path('transacciones/', include('transacciones.urls')),
    path('presupuesto/', include('presupuesto.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('chatbot/', include('chatbot.urls')),
]