from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView  
from django.utils.decorators import method_decorator 
from user.decorators import login_required, admin_required
from django.db import transaction 
from .forms import RegisterForm 
from .models import Order 
from product.models import Product
from user.models import User 

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm 
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=prod,
                user=User.objects.get(email=self.request.session.get('user'))
            )
            order.save() 
            prod.stock -= int(form.data.get('quantity')) 
            prod.save()
        
        return super().form_valid(form)

    def form_invalid(self, form):
        # 실패를 했을 경우 error message를 보여주기 위한 page 지정 
        return redirect('/product/' + str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):
        #order forms.py에서 def __init__의 request를 product의 views.py에 보내기 위해
        #form을 생성할때 어떤 인자 값을 전달해서 만들건지 결정하는 함수
        kw = super().get_form_kwargs(**kwargs) #formview가 생성하는 인자값
        kw.update({
            #request인자값도 보내준다
            'request': self.request
        })
        return kw 

@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    # model = Order #모든 사람의 정보를 볼 수 있다

    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        #로그인 되어있는 사람의 구매 정보만 보게 하는 방법
        queryset = Order.objects.filter(user__email=self.request.session.get('user'))
        return queryset