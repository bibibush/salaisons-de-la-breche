from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.generic.edit import BaseUpdateView

from users.form import ContactForm
from users.models import Users
from django.views import View

from users.utils import obj_to_contact


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
        'first_name',
        'last_name',
        'entreprise',
        'phonenumber',
        'adresse',
    )
    
    def form_valid(self, form):
        self.object = form.save()
        post = {
            'email' : self.object.email,
            'nom': self.object.first_name,
            'prenom': self.object.last_name,
            'entreprise' : self.object.entreprise,
            'phonenumber' : self.object.phonenumber,
            'adresse' : self.object.adresse,
                }
        
        return JsonResponse(data=post, safe=True, status= 200)
    def form_invalid(self, form):
        return JsonResponse(data=form.errors, safe=True, status=400)

class ContactView(View):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = form.save()
            post = obj_to_contact(obj)
            title = f"Contact via site internet {post['create_dt']}"
            title_client = "Confirmation d'envoi"
            content = (f"<p><strong>Nom : </strong>{post['nom']}</p>"
                       f"<p><strong>Prenom : </strong>{post['prenom']}</p>"
                       f"<p><strong>Numero de Téléphone : </strong>{post['number']}</p>"
                       f"<p><strong>Email : </strong>{post['email']}</p>"
                       f"<p><strong>Objet : </strong>{post['sujet']}</p>"
                       f"<br />"
                       f"<strong>La demande : </strong>"
                       f"<br />"
                       f"<p>{post['question']}</p>")
            content_client = (f"<p>Bonjour,</p>"
                              f"<p>Votre demande ci-dessous a bien été envoyée.</p>"
                              f"<br />"
                              f"<strong>{post['question']}</strong>"
                              f"<br />"
                              f"<br />"
                              f"<p>Elle sera traitée dans les meilleurs délais.</p>"
                              f"<p>Cordialement,</p>"
                              f"<P>SALAISONS DE LA BRÈCHE</P>")
            email = EmailMessage(subject=title, body=content, to=['contact@salaisonsdelabreche.com', 'salaisons.de.la.breche@orange.fr'])
            email2 = EmailMessage(subject=title_client, body=content_client, to=[post['email']])
            email.content_subtype="html"
            email2.content_subtype= "html"
            email.send()
            email2.send()
            return JsonResponse(data=post, safe=True, status=200)
        else:
            return JsonResponse(data=form.errors, safe=True, status=400)

