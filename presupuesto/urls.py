from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_presupuestos, name='presupuesto'),
    path('nuevo/', views.nuevo_presupuesto, name='nuevo_presupuesto'),
    path('eliminar/<int:pk>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
]