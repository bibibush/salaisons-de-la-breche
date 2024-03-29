from typing import Any
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import BaseCreateView, BaseUpdateView, BaseDeleteView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model, get_user
from django.core.files.storage import FileSystemStorage
from api.models import Order, File
from users.models import Users
from users.views import MyLoginRequiredMixin, OwnerOnlyMixin, AdminOnlyMixin
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from api.views_utils import obj_to_order
from api.views_utils import random_letters
from django.views import View
from api.form import LoginForm, RegisterForm
import urllib
import mimetypes
import os
from datetime import date, timedelta
from django.core.mail import EmailMessage

# Create your views here.
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ApiView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={}, safe=False, status=200)

class ApiLoginView(View):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Users.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                userDict = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
                return JsonResponse(data=userDict, safe=True, status=200)
        else:
            JsonResponse(data=form.errors, safe=True, status=400)


class ApiLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse(data={}, safe=True, status=200)


class RegisterView(BaseCreateView):
    form_class = RegisterForm

    def form_valid(self, form):
        form.instance.username = form.instance.first_name
        self.object = form.save()
        user_dict = {
            'username': self.object.first_name,
            'email': self.object.email,
        }

        return JsonResponse(data=user_dict, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class GetMe(View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if user.is_authenticated:
            userDict = {
                'id': user.id,
                'username': user.username,
                'nom': user.first_name,
                'prenom': user.last_name,
                'email': user.email,
                'entreprise': user.entreprise,
                'phonenumber': user.phonenumber,
                'adresse': user.adresse
            }
        else:
            userDict = {
                'username': '',
                'nom': '',
                'prenom': '',
                'email': '',
                'entreprise': '',
                'phonenumber': '',
                'adresse': ''
            }
        return JsonResponse(data=userDict, safe=True, status=200)


class ApipwdChangeView(PasswordChangeView):
    def form_valid(self, form):
        new_pw = form.cleaned_data.get('new_password1')
        old_pw = form.cleaned_data.get('old_password')
        if new_pw == old_pw:
            update_session_auth_hash(self.request, form.user)
            return JsonResponse(data=form.errors, safe=True, status=401)
        form.save()
        update_session_auth_hash(self.request, form.user)
        return JsonResponse(data={}, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class ApiFileDownloadView(MyLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        object = File.objects.get(title='first')
        file_path = object.file.path
        file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename= {os.path.basename(file_path)}'
        return response

class ApiBonDownloadView(MyLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        object = File.objects.get(title='bon')
        file_path = object.file.path
        file_type = 'application/pdf'
        with open(file_path, 'rb') as f:
            content = f.read()
            response = HttpResponse(content ,content_type = file_type)
            response['Content-Disposition'] = f'attachment; filename= {os.path.basename(file_path)}'
            return response

class ApiFileUploadView(MyLoginRequiredMixin, BaseCreateView):
    model = Order
    fields = '__all__'

    def form_valid(self, form):
        qs = Order.objects.all()
        form.instance.user = self.request.user
        form.instance.order_number = random_letters(10)
        for obj in qs:
            while form.instance.order_number == obj.order_number:
                form.instance.order_number = random_letters(10)
        bon = form.save()
        post = obj_to_order(bon)
        title = 'Votre commande est bien passé'
        content = "Votre commande Nº" + post['order_number'] + " est bien passé. \nVotre commande arrive environ " + \
                  post['date'] + "\nMerci"
        email = EmailMessage(subject=title, body=content, to=[post['email']])
        email.send()
        return JsonResponse(data=post, safe=True, status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class ApiCommandeInfoView(OwnerOnlyMixin, BaseDetailView):
    model = Order

    def render_to_response(self, context, **response_kwargs):
        self.object = context['object']
        if date.today() >= self.object.date - timedelta(days=14) and not self.object.pay:
            self.object.paspaye = True
        elif date.today() >= self.object.date - timedelta(days=14) and self.object.pay:
            self.object.validable = True
            if date.today() >= self.object.date and self.object.pay:
                self.object.done = True
        if date.today() >= self.object.date - timedelta(days=14):
            self.object.block = True
        post = obj_to_order(self.object)
        return JsonResponse(data=post, safe=True, status=200)


class ApiCommandeManageView(OwnerOnlyMixin, BaseDetailView):
    model = Order

    def render_to_response(self, context, **response_kwargs):
        self.object = context['object']
        post = obj_to_order(self.object)
        return JsonResponse(data=post, safe=True, status=200)

class ApiAdminCommandeManageView(AdminOnlyMixin, BaseDetailView):
    model = Order

    def render_to_response(self, context, **response_kwargs):
        self.object = context['object']
        post = obj_to_order(self.object)
        return JsonResponse(data=post, safe=True, status=200)


class ApiCommandExcelView(OwnerOnlyMixin, BaseDetailView):
    model = Order

    def get(self, request, pk, *args, **kwargs):
        object = Order.objects.get(pk=pk)
        file_path = object.order_file.path
        file_name = urllib.parse.quote(object.order_file.name.encode('utf-8'))
        # file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'%s' % file_name
        return response

class ApiCommandeListView(MyLoginRequiredMixin, BaseListView):
    def get_queryset(self):
        qs = Order.objects.filter(user__email=self.request.user.email).order_by('-create_dt')
        return qs
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_order(obj) for obj in qs]
        return JsonResponse(data=postList, safe=False, status=200)

class ApiAdminListView( AdminOnlyMixin, BaseListView ):
    def get_queryset(self):
        if self.request.user.email == 'contact@salaisonsdelabreche.com':
            qs = Order.objects.all().order_by('-create_dt')
        else:
            qs = []
        return qs

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        for obj in qs:
            if date.today() >= obj.date - timedelta(days=14) and not obj.pay:
                obj.paspaye = True
            elif date.today() >= obj.date - timedelta(days=14) and obj.pay:
                obj.validable = True
                if date.today() >= obj.date and obj.pay:
                    obj.done = True
            
        postList = [obj_to_order(obj) for obj in qs]
        return JsonResponse(data=postList, safe=False, status=200)

class ApiInfoUpdateView(MyLoginRequiredMixin, OwnerOnlyMixin, BaseUpdateView):
    model = Order
    fields = (
        'nom',
        'prenom',
        'adresse',
        'phonenumber',
        'entreprise',
        'email',
    )

    def form_valid(self, form):
        self.object = form.save()
        post = obj_to_order(self.object)
        title = 'Votre commande est bien modifié'
        content = f'Votre commande Nº{post["order_number"]} est bien modifié. \nVotre commande arrive environ \
                  {post["date"]} \nMerci'
        email = EmailMessage(subject=title, body=content, to=[post['email']])
        email.send()
        return JsonResponse(data=post, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class ApiExcelUpdateView(MyLoginRequiredMixin, OwnerOnlyMixin, BaseUpdateView):
    model = Order
    fields = (
        'order_file',
    )

    def form_valid(self, form):
        self.object = form.save()
        post = obj_to_order(self.object)
        title = 'Votre commande est bien modifié'
        content = f'Votre commande Nº{post["order_number"]} est bien modifié. \nVotre commande arrive environ \
                  {post["date"]} \nMerci'
        obj = self.get_object()
        to = obj.email
        email = EmailMessage(subject=title, body=content, to=[to])
        email.send()
        return JsonResponse(data=post, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class ApiDateUpdateView(MyLoginRequiredMixin, OwnerOnlyMixin, BaseUpdateView):
    model = Order
    fields = (
        'date',
    )

    def form_valid(self, form):
        self.object = form.save()
        post = obj_to_order(self.object)
        title = 'Votre commande est bien modifié'
        content = f'Votre commande Nº{post["order_number"]} est bien modifié. \nVotre commande arrive environ \
                  {post["date"]} \nMerci'
        obj = self.get_object()
        to = obj.email
        email = EmailMessage(subject=title, body=content, to=[to])
        email.send()
        return JsonResponse(data=post, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)


class ApiPayUpdateView(MyLoginRequiredMixin, OwnerOnlyMixin, BaseUpdateView):
    model = Order
    fields = (
        'pay',
    )

    def form_valid(self, form):
        self.object = form.save()
        post = obj_to_order(self.object)
        title = 'Votre payment est bien verifié'
        content = f'Votre commande Nº{post["order_number"]} est bien payé. \nVotre commande arrive environ \
                  {post["date"]} \nMerci'
        obj = self.get_object()
        email = EmailMessage(subject=title, body=content, to=[obj.email])
        email.send()
        return JsonResponse(data=post, safe=True, status=200)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ApiDeleteView(BaseDeleteView, OwnerOnlyMixin):
    model = Order
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        os.remove(self.object.order_file.path)
        self.object.delete()
        return JsonResponse(data={}, safe=True, status=204)
