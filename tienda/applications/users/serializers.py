

from rest_framework import serializers

class LoginSocialSerializer(serializers.Serializer):
    # print('antes token_id')
    token_id = serializers.CharField(required = True)
    # print('despues token_id')
