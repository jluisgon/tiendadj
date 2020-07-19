

from rest_framework import viewsets

from rest_framework.response import Response

from .models import Colors, Product

from .serializers import (
    ColorsSerializer,
    PoductSerializer, 
    PaginationSerializer,
    PoductSerializerViewSet
)

class ColorViewSet(viewsets.ModelViewSet):
    
    # ya estas dos lineas de codigo que es CRUD
    
    serializer_class = ColorsSerializer
    # los viewset siempre necesitan de este parametro queryset
    queryset = Colors.objects.all()
    
    
class ProductViewSet(viewsets.ModelViewSet): 
    
    serializer_class = PoductSerializerViewSet  
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer
    
    
    # sobreesribir metodo al crear 
    # se comenta por Perform_created
    # def create (self, request):
    #    print(request.data)
    #    return Response ({'code': 'ok'})
    
    # Perform_created indica que va suceder antes que se guarden los datos
    # aqui esta haciendo el guardado de los datos del serializador
    # serializer ya esta como un objeto
    def perform_create(self, serializer):
        # guardar algun valor anes de guardarlo en la bd     
        serializer.save(
            video = "https://www.youtube.com/watch?v=dqELwe0Htsc&t=7s"
        )
        
    # se sobreescribe esta funcion para ver el litado de productos por usuario  
    # queryset = Product.objects.all() ya no es todo ya es por usuario  
    def list(self, request, *args, **kwargs):
        queryset = Product.objects.productos_por_user(self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)