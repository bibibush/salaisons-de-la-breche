from typing import Any
from django.shortcuts import render
from django.views.generic.edit import BaseCreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model, get_user
from django.core.files.storage import FileSystemStorage
from api.models import Order, File
from users.models import Users
from users.views import MyLoginRequiredMixin
from django.http import HttpResponse, JsonResponse, FileResponse
from api.views_utils import obj_to_order
from django.views import View
from api.form import LoginForm, RegisterForm
import os

# Create your views here.
class ApiPostV(BaseCreateView):
    model = Order
    fields = (
        "name",
        "adresse",
        "order_list",
    )
 
    def form_valid(self, form):
        self.object = form.save()
        post = obj_to_order(self.object)
        return JsonResponse(data=post, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ApiLoginView(View):

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = Users.objects.get(email=email)
            user.check_password(password)
            login(self.request, user)
            userDict = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            return JsonResponse(data=userDict, safe=True, status=200)
        else:
            JsonResponse(data=form.errors, safe=True, status=400)
    
class ApiLogoutView(LogoutView):
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse(data={}, safe=True, status=200)
        
class RegisterView(BaseCreateView):
    form_class = RegisterForm

    def form_valid(self, form):
        self.object = form.save()
        userDict = {
            'username': self.object.username,
            'email': self.object.email,
        }
        
        return JsonResponse(data=userDict, safe=True, status=201 )

    def form_invalid(self,form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class GetMe(View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if user.is_authenticated:
            userDict = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        else:
            userDict= {
                'username': 'annonymous'
            }
        return JsonResponse(data=userDict, safe=True, status=200)

class ApipwdChangeView(PasswordChangeView):
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)

        return JsonResponse(data={}, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse (data=form.errors, safe=True, status= 400)

class ApiFileDownloadView(MyLoginRequiredMixin,View):        
    
    def get(self, request, *args, **kwargs):
        object = File.objects.get(title = 'first')
        file_path = object.file.path
        file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type= file_type)
        response['Content-Disposition'] = f'attachment; filename=' + os.path.basename(file_path)
        return response
