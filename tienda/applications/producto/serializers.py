
from rest_framework import serializers

from .models import Product, Colors

class ColorsSerializer(serializers.ModelSerializer):
    #print ('antes PoductSerializer')   
     
    class Meta:
        model = Colors
        fields = (
            'color',
        )

class PoductSerializer(serializers.ModelSerializer):
    #print ('antes PoductSerializer')   
    
    colors = ColorsSerializer(many = True)
     
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'man',
            'woman',
            'weight',
            'price_purchase',
            'price_sale',
            'main_image',
            'image1',
            'image2',
            'image3',
            'image4',
            'colors',
            'video',
            'stok',
            'num_sales',
            'user_created'
        )
        
        #print ('despues PoductSerializer')   