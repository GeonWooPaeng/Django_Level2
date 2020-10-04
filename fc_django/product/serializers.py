from rest_framework import serializers 
from .models import Product 

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        #모델 연결
        model = Product 
        fields ='__all__' #자동으로 model안의 모든 field를 가지고 온다.