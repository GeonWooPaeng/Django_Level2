from django import forms
from .models import Order 
from user.models import User 
from product.models import Product
# Create your views here.

class RegisterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        # form에서 request를 전달 받을 수 있게 하기 위함 -> session에 접근할 수 있게 하는 것
        super().__init__(*args, **kwargs)
        self.request = request 

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력해주세요.'
        }, label='수량'
    )
    product = forms.IntegerField(
        error_messages={
            'required': '상품설명을 입력해주세요.'
        }, label='상품설명', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        #저장하는 부분 
        quantity = cleaned_data.get('quantity') #수량가져오기
        product = cleaned_data.get('product')
        
        # user의 views.py에서 def form_valid에서의 request.session['여기부분']을 써준다 
        # user을 가져온다
        user = self.request.session.get('user')

        if quantity and product and user:
            order = Order(
                quantity=quantity,
                product=Product.objects.get(pk=product),
                user=User.objects.get(email=user)
            ) 
            order.save()

        else:
            self.product = product 
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
