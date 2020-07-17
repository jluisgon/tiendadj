

from django.urls import path

from . import views

app_name = 'venta_app'

urlpatterns = [
    path('api/venta/reporte/',
         views.ReporteVentasList.as_view(),
         name = 'venta-reporte'
    ),
    path('api/venta/create/',
         views.RegistraVenta.as_view(),
         name = 'venta-register'
    ),  
    path('api/venta/add/',
         views.RegistraVenta2.as_view(),
         name = 'venta-add'
    ),  
 
 
]
