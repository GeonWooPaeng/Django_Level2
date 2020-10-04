from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import FormView 
from django.utils.decorators import method_decorator 
from rest_framework import generics 
from rest_framework import mixins 

from user.decorators import login_required, admin_required
from .models import Product 
from .forms import RegisterForm
from .serializers import ProductSerializer
from order.forms import RegisterForm as OrderForm
# Create your views here.

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer #데이터 검증

    def get_queryset(self):
        #어떤 data를 가지고 올 것인지(모두)
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer 

    def get_queryset(self):
        return Product.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ProductList(ListView):
    model = Product 
    template_name = 'product.html' #template 지정
    context_object_name = 'product_list' #object_list 지정

@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm 
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)

class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all() #모든 제품 가져오기
    context_object_name = 'product'

    #DetailView에다가 form을 전달해주는 방식
    #원하는 data를 넣을수 있는 함수
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request) #order forms.py에서 def __init__에서 request받아온다. 
        return context