
from rest_framework import serializers

from .models import Sale, SaleDetail


class VentaReporteSerializers(serializers.ModelSerializer):

    # nuevo atributo que no esta en el modelo
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'productos'
        )

    def get_productos(self, obj):
        query = SaleDetail.objects.productos_por_venta(obj.id)
        productos_serializados = DetalleVentaProductoSerializer(query, many = True).data
        return productos_serializados


class DetalleVentaProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale'                
        )
