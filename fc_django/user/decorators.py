from django.shortcuts import redirect 
from .models import User 

def login_required(function):
    def wrap(request, *args, **kwargs):
        #로그인 확인 
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')
        return function(request, *args, **kwargs) 
        
    return wrap 

def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')

        user = User.objects.get(email=user) # 유저 정보 가져오기
        if user.level != 'admin':
            return redirect('/')
        
        return function(request, *args, **kwargs)

    return wrap