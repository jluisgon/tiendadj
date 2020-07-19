

from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from applications.producto.models import Product

from .serializers import ProcesoVentaSerializer2, VentaReporteSerializers

from .models import Sale, SaleDetail


class VentasViewSet(viewsets.ViewSet): 
    
    #es lo viewsets.ViewSet no es necesario
    #serializer_class = VentaReporteSerializers
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = Sale.objects.all()
        # serializar datos
        serializer = VentaReporteSerializers(queryset, many=True)
        # solo retornanos los datos ya que es un objeto
        return Response(serializer.data)
    
    def create(self, request):
        # deserializar el json que recibimos
        serializer = ProcesoVentaSerializer2(data = request.data)
        # verificar si lo que nos envian es valido y esta como indica el serializer ProcesoVentaSerializer2
        # si hay un error manda una excepcion
        serializer.is_valid(raise_exception = True)          
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