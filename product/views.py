from django.db.migrations import serializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Product, Cart
from rest_framework.views import APIView
from .serializers import ProductSerializer, CartSerializer,UpdateSerializer
from rest_framework import permissions, status
# from account.permissions import IsVendor


class ProductListApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request):
        products=Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCartAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]
    def get(self,request,id):
        cart=Cart.objects.get(user_id=id)
        product=cart.product.all()
        serializer2=ProductSerializer(product, many=True)
        serializer=CartSerializer(cart)
        data=serializer.data
        data['product']=serializer2.data
        return Response(data)

    def put(self, requests, id):
        cart = self.get_object(id)
        serializer = UpdateSerializer(cart, data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



