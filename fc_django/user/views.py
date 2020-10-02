from django.shortcuts import render, redirect
from django.views.generic.edit import FormView 
from .forms import RegisterForm, LoginForm

# Create your views here.

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/' #success하면 '/'로 이동

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm 
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.email 

        return super().form_valid(form) #기존의 form_valid함수 추가


#로그아웃 기능 -> urls에 연결
def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')