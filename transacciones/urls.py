from django.urls import path
from . import views

urlpatterns = [
    path('gastos/', views.lista_gastos, name='gastos'),
    path('gastos/nuevo/', views.nuevo_gasto, name='nuevo_gasto'),
    path('gastos/editar/<int:pk>/', views.editar_gasto, name='editar_gasto'),
    path('gastos/eliminar/<int:pk>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('ingresos/', views.lista_ingresos, name='ingresos'),
    path('ingresos/nuevo/', views.nuevo_ingreso, name='nuevo_ingreso'),
    path('ingresos/editar/<int:pk>/', views.editar_ingreso, name='editar_ingreso'),
    path('ingresos/eliminar/<int:pk>/', views.eliminar_ingreso, name='eliminar_ingreso'),
    path('reporte/', views.selector_reporte, name='selector_reporte'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
]