from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chatbot'),
    path('enviar/', views.enviar_mensaje, name='chat_enviar'),
]