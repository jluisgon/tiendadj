
# libreria para la fecha del servidor de la confifuracion
from django.utils import timezone

from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from .models import Sale, SaleDetail

from applications.producto.models import Product

from .serializers import (
    VentaReporteSerializers,
    ProcesoVentaSerializer,
    ProcesoVentaSerializer2
) 

# Create your views here.


class ReporteVentasList(ListAPIView):
    
    serializer_class = VentaReporteSerializers
    
    def get_queryset(self):
        return Sale.objects.all()
    
class RegistraVenta(CreateAPIView):
    """ Clase para registrar una venta """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    serializer_class = ProcesoVentaSerializer
    
    # sobreescribir esta funcion
    # por el metodo post entra a esta funcion
    def create (self, request, *args, **kwargs):
        # deserializar el json que recibimos
        # serializer puede ser cualquier nombre
        # recuperamos lo que esta en el request -> request.data
        serializer = ProcesoVentaSerializer(data = request.data)
        # verificar si lo que nos envian es valido y esta como indica el serializer ProcesoVentaSerializer
        # si hay un error manda una excepcion
        serializer.is_valid(raise_exception = True)   
        # solo probar a ver si va retornando algo    
        # solo se puede usar serializer.validated_data si usuamos esto serializer.is_valid
        # tipo_recibo = serializer.validated_data['type_invoce']         
        # print('***', tipo_recibo)
        
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce=  serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,            
        )
        # variables para la venta
        amount = 0
        count = 0
        # recuperamos los productos de la venta y es una coleccion
        productos = serializer.validated_data['productos']
        # print (productos)
        ventas_detalle = []
        for producto in productos:
            prod = Product.objects.get(id = producto['pk'])
            # se crea un objeto venta_detalle
            venta_detalle = SaleDetail(
               sale = venta,
               product = prod,
               count =  producto['count'],
               price_purchase = prod.price_purchase,
               price_sale = prod.price_sale,
            )
            amount = amount + prod.price_sale * producto['count']
            count = count + producto['count']
            ventas_detalle.append(venta_detalle)
            
        venta.amount = amount
        venta.count = count
        venta.save()    
        SaleDetail.objects.bulk_create(ventas_detalle)
        return Response ({'msj': 'Venta Exitosa'})
    
    
class RegistraVenta2(CreateAPIView):
    """ Clase para registrar una venta """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    serializer_class = ProcesoVentaSerializer2
    
    # sobreescribir esta funcion
    # por el metodo post entra a esta funcion
    def create (self, request, *args, **kwargs):
        # deserializar el json que recibimos
        # serializer puede ser cualquier nombre
        # recuperamos lo que esta en el request -> request.data
        serializer = ProcesoVentaSerializer2(data = request.data)
        # verificar si lo que nos envian es valido y esta como indica el serializer ProcesoVentaSerializer2
        # si hay un error manda una excepcion
        serializer.is_valid(raise_exception = True)   
        # solo probar a ver si va retornando algo    
        # solo se puede usar serializer.validated_data si usuamos esto serializer.is_valid
        # tipo_recibo = serializer.validated_data['type_invoce']         
        # print('***', tipo_recibo)
        
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce=  serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,            
        )
        # variables para la venta
        amount = 0
        count = 0
        # recuperamos todos los productos en la bd con todos los productos (id) que tiene el array productos 
        productos = Product.objects.filter(
            id__in = serializer.validated_data['productos']
        )
        # recuperamos el array de cantidades
        cantidades = serializer.validated_data['cantidades']
        # print (productos)
        ventas_detalle = []
        # se itera dos listas
        for producto, cantidad in zip(productos, cantidades):           
            # se crea un objeto venta_detalle
            venta_detalle = SaleDetail(
               sale = venta,
               product = producto,
               count =  cantidad,
               price_purchase = producto.price_purchase,
               price_sale = producto.price_sale,
            )
            amount = amount + producto.price_sale * cantidad
            count = count + cantidad
            ventas_detalle.append(venta_detalle)
            
        venta.amount = amount
        venta.count = count
        venta.save()    
        SaleDetail.objects.bulk_create(ventas_detalle)
        return Response ({'msj': 'Venta Exitosa'})