from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView 
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import User 

# Create your views here.

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/' #success하면 '/'로 이동

    def form_valid(self, form):
        #유효성 검사 끝났을 때 user생성 
        user = User(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level='user'
        )
        user.save()

        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm 
    success_url = '/'

    def form_valid(self, form):
        # self.request.session['user'] = form.email 
        self.request.session['user'] = form.data.get('email')

        return super().form_valid(form) #기존의 form_valid함수 추가


#로그아웃 기능 -> urls에 연결
def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')