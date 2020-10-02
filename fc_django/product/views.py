from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import FormView 
from django.utils.decorators import method_decorator 
from user.decorators import login_required
from .models import Product 
from .forms import RegisterForm
from order.forms import RegisterForm as OrderForm
# Create your views here.

class ProductList(ListView):
    model = Product 
    template_name = 'product.html' #template 지정
    context_object_name = 'product_list' #object_list 지정

@method_decorator(login_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm 
    success_url = '/product/'

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