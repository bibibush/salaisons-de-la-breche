# Salaisons de la Brèche
## Backend

고객들이 웹사이트를 통해 문의하고 메일이 잘 전송되었는지 자동으로 확인받는
컨텍트 기능을 구현하기 위해서 users 앱에 있는 models.py에 Contact 모델을
작성
```commandline
class Contact(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    create_dt = models.DateTimeField(blank=True)
    sujet = models.CharField(max_length=250, null=True, blank=True)
    question = models.TextField()

    def __str__(self):
        return self.nom

# nom, prenom 은 성, 이름 그리고 sujet는 메일의 제목입니다.
```
고객이 작성한 내용을 담을 수 있는 ContactForm을 모델 Form을 이용해서 작성
```commandline
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
```
Django의 EmailMessage를 사용하기 위해 settings.py 에서 gmail에 맞는 필요 코드 작성.
```commandline
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = 'contact@salaisonsdelabreche.com'
EMAIL_HOST_PASSWORD = os.getenv("APP_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
ContactView 작성
```commandline
class ContactView(View):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.instance.create_dt = datetime.datetime.now(pytz.timezone("Europe/Paris"))
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
```
obj_to_contact 함수를 만들어서 데이터들을 딕셔너리 객체로 변환
```commandline
def obj_to_contact(obj):
    post = dict(vars(obj))
    if post['sujet'] is None:
        post['sujet'] = ""

    if obj.create_dt:
        post['create_dt'] = obj.create_dt.strftime('%d/%m/%Y %H:%M')
    else:
        post['create_dt'] = ''

    del post['_state']

    return post
```
ContactView에서 메일 생성시간을 제목 옆에 나타냄으로서 회사 이메일 보관함에 메일이 겹쳐서 보이지 않도록 처리했습니다.
<br />고객이 회사로 보내는 문의메일은 email, 자동으로 회사에서 고객한테 보내는 답장메일은 email2로 담아서 send 메소드로 기능을 구현했습니다.

* 웹사이트 문의하기 페이지: https://www.salaisonsdelabreche.com/contact/





