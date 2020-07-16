from rest_framework.generics import (
    ListAPIView
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import render

from .serializers import PoductSerializer

from .models import Product

# Create your views here.


class ListProductUser(ListAPIView):
    serializer_class = PoductSerializer
    # rest_framework.authtoken  ya trae complementos para desenciprtar el token e indentificar al usuario
    # authentication_classes indentificar o autenticar so es o no es usuario, pero no interfiere las lineas de codigo
    # TokenAuthentication que tipo de autentificacion se quiere
    authentication_classes = (TokenAuthentication,)
    # permission_classes que tipo de permiso tendra esta vista, si interfiere que se cargue o no se cargue la vista
    # IsAuthenticated tipo de permiso, que la vista se cargue si el token esta correctamente autenticado o verificado
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        print(usuario)
        return Product.objects.productos_por_user(usuario)


class ListProductoStok(ListAPIView):
    serializer_class = PoductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Product.objects.productos_con_stok()


class ListProductoGenero(ListAPIView):
    serializer_class = PoductSerializer

    def get_queryset(self):
        # recupera el parametro que viene por la url
        genero = self.kwargs['gender']
        return Product.objects.productos_por_genero(genero)


class FiltrarProductos(ListAPIView):
    
    serializer_class = PoductSerializer
    
    def get_queryset(self):
        # se recupera valores que vienen por get
        # variable man y None (ya que se puede recibir mas parammetros)      
        varon = self.request.query_params.get('man', None)
        mujer = self.request.query_params.get('woman', None)
        nombre = self.request.query_params.get('name', None)
        return Product.objects.filtar_productos(
            man = self.request.query_params.get('man', None),
            woman = mujer,
            name = nombre
        )