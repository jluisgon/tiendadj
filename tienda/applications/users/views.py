from rest_framework.views import APIView
# se importa el modelo Token
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from firebase_admin import auth

from django.shortcuts import render

from django.views.generic import TemplateView

from .serializers import LoginSocialSerializer

from .models import User

# Create your views here.

class LoginUser(TemplateView):
    template_name = "users/login.html"


class GoogleLoginView(APIView):
    
    #print('antes serializer_class')
    serializer_class = LoginSocialSerializer
    #print('despues serializer_class')
     
    def post (self, request):
        #print('antes post')
        # recuperar la iformacion que envian del serividor
        # se serializa la data --> self.serializer_class(data = request.data)
        serializer = self.serializer_class(data = request.data)
        # valido que la informacion es correcta
        serializer.is_valid(raise_exception=True)
        # recupero token_id del serializars.py
        id_token = serializer.data.get('token_id')     
        # decodifcar el id_token  
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token['email']
        name = decoded_token['name']
        avatar = decoded_token['picture']
        verified = decoded_token['email_verified']
        
        usuario, created = User.objects.get_or_create(
            email = email,
            defaults = {
                'full_name' : name,
                'email' : email,
                'is_active' : True
            }
        )
        #
        if created:
            # modelo Token
            token = Token.objects.create(user = usuario)
        else:
            token = Token.objects.get(user = usuario)
        
        # userGet es un objeto javascript y es lo que espera el front end formato json
        userGet = {
            'id' : usuario.pk,
            'email' : usuario.email,
            'full_name' : usuario.full_name,
            'genero' :  usuario.genero,
            'date_birth': usuario.date_birth,
            'city' : usuario.city
        }
        #print('despues post')
        return Response (
            {
                 # Token e sun objeto y solo se requiere enviar la clave
                'token' : token.key,
                'user' : userGet
            }
        )
    
    