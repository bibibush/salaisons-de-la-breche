from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import JsonResponse

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
        