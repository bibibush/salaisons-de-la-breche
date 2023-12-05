from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import JsonResponse
from django.views.generic.edit import BaseUpdateView
from users.models import Users

# Create your views here.

class MyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {'message' : "vous n'avez pas droit à télécharger, Connectez-vous s'il vous plait"}
            return JsonResponse(data=data, safe=True, status=401)
        return super().dispatch(request, *args, **kwargs)

class OwnerOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.email != self.object.user.email and request.user.email != 'contact@salaisonsdelabreche.com':
            data = {'message': "Vous n'avez pas droit"}
            return JsonResponse(data=data, safe=True, status=403)
        return super().dispatch(request, *args, **kwargs)
        
class AdminOnlyMixin(LoginRequiredMixin, AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.email != 'contact@salaisonsdelabreche.com':
            data = {'message': "Vous n'avez pas droit"}
            return JsonResponse(data=data, safe=True, status=401)
        return super().dispatch(request, *args, **kwargs)

class UserInfoUpdate(BaseUpdateView):
    model = Users
    fields = (
        'email',
        'entreprise',
        'phonenumber',
        'adresse',
    )
    
    def form_valid(self, form):
        self.object = form.save()
        post = {
            'email' : self.object.email,
            'entreprise' : self.object.entreprise,
            'phonenumber' : self.object.phonenumber,
            'adresse' : self.object.adresse,
                }
        
        return JsonResponse(data=post, safe=True, status= 200)
    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)