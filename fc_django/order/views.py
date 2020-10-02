from django.shortcuts import render, redirect
from django.views.generic.edit import FormView 
from .forms import RegisterForm 

class OrderCreate(FormView):
    form_class = RegisterForm 
    success_url = '/product/'

    def form_invalid(self, form):
        # 실패를 했을 경우 error message를 보여주기 위한 page 지정 
        return redirect('/product/' + str(form.product))

    def get_form_kwargs(self, **kwargs):
        #order forms.py에서 def __init__의 request를 product의 views.py에 보내기 위해
        #form을 생성할때 어떤 인자 값을 전달해서 만들건지 결정하는 함수
        kw = super().get_form_kwargs(**kwargs) #formview가 생성하는 인자값
        kw.update({
            #request인자값도 보내준다
            'request': self.request
        })
        return kw 