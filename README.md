# Salaisons de la Brèche
## Backend
#### 소개
Salaisons de la Brèche라는 회사는 돼지고기를 가공해 만든 식품인 Saucisson( 쏘시쏭 )을 제조하는 회사입니다.
<br />회사가 추구하는 웹사이트의 목적은 고품질 재료와 전통적인 방법을 사용한 제품생산이라는 사실을 강조하는것 입니다. 또한 제품관련 문의를 많이 받기 때문에 프론트엔드에서 회사 연락처와 문의하기 페이지를 웹사이트에 잘 나타나도록 했습니다.

백엔드 서버에서는 문의하기, login, 첨부파일 다운로드와 전송, 
주문정보 보내기 등의 기능들을 구현했습니다.
<br />모든 기능들이 잘 동작하지만 지금 서비스 되고 있는 기능은 문의하기 기능 하나입니다.

---
#### 프로젝트 구조
```commandline
- salaisons-de-la-breche(프로젝트 파일)
    - api
    - users
    - client
        - index.html
        - static
    - media
        - upload
        - Bon_de_commande_CSE_-_SALAISONS_DE_LA_BRECHE.pdf
        - MODELE_Tableau_CSE_2022.xlsx
    - mysite
        - settings.py
        - urls.py
```
api와 users 두개의 앱을 생성해 로그인, 주문 관련 기능들은 api앱 안에 작성했고 사용자 관련한 기능들은 users 앱 안에서 코드를 작성했습니다.

client 폴더는 일반적인 Django의 Templates 폴더를 대체하는 폴더입니다.

media 폴더는 고객들이 주문하기 위해 필요한 주문양식서들이 있고 고객들이 주문서를 제출할 때 주문서들이 upload 폴더 안으로 갈 수 있도록 api앱 models.py에서 설정했습니다.
```commandline
class Order(models.Model):
    ...
    order_file = models.FileField(upload_to='upload/', null=True,)
    ...
```
---
### 기능들
- 이 Django 프로젝트에 있는 모든 기능을 보여드리는 것이 아닌 웹사이트에서 중요한 몇 가지 기능을 밑에 서술하였습니다.

---

#### 문의하기 기능
고객들이 웹사이트를 통해 문의하고 메일이 잘 전송되었는지 자동으로 확인받는
컨텍트 기능을 구현하기 위해서 users 앱에 있는 models.py에 Contact 모델을
작성했습니다.
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
고객이 작성한 내용을 담을 수 있는 ContactForm을 모델 Form을 이용해서 작성.
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
ContactView 작성.
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
obj_to_contact 함수를 만들어서 데이터들을 딕셔너리 객체로 변환.
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

---
#### 로그인 및 비밀번호 변경
users앱의 models.py에 유저 관련 모델을 만들었습니다.
```commandline
class Users(AbstractUser):
    email = models.EmailField(_('email adress'), unique=True)
    entreprise = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=20)
    adresse = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    def __str__(self):
        return self.username
```
abstractUser를 사용했지만 로그인을 할 때 username이 아닌 이메일로 로그인 할 수 있도록 작성하였습니다.

로그인 폼
```commandline
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=30)
```
로그인 view
```commandline
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
```
비밀번호 변경 view
```commandline
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
```
---
#### 첨부파일(주문서 양식) 다운로드
api앱 models.py에 File 모델을 작성했습니다.
```commandline
class File(models.Model):
    title = models.CharField(max_length=30, null=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.title
```
다운로드 view
```commandline
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
```
이 코드에서 다루고 있는 파일은 pdf 파일임으로 file_type으로 pdf에 맞게 작성했습니다.
<br />이 다운로드view는 MyLoginRequiredMixin을 상속받는데 이 믹스인은 로그인을 한 상태여야만 다운로드 기능이 동작하게끔 LoginRequiredMixin을 상속받아서 작성했습니다.
```commandline
# users/views.py

class MyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {'message' : "vous n'avez pas droit à télécharger, Connectez-vous s'il vous plait"}
            return JsonResponse(data=data, safe=True, status=401)
        return super().dispatch(request, *args, **kwargs)
```
---
#### 제품 주문

주문 관련한 Order model을 api앱안에 작성
```commandline
class Order(models.Model):
    nom = models.CharField('nom',max_length=50)
    prenom = models.CharField('prenom',max_length=50)
    adresse = models.CharField('adresse',max_length=50)
    phonenumber = models.CharField('phonenumber',max_length=50)
    entreprise = models.CharField('entreprise',max_length=100)
    user = models.ForeignKey(Users,on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField('email',max_length=50)
    create_dt = models.DateTimeField('create date',auto_now_add=True)
    modify_dt = models.DateField('modify date',auto_now=True)
    order_file = models.FileField(upload_to='upload/', null=True,)
    order_number = models.CharField('order number',max_length=10, blank=True)
    date = models.DateField(null=True)
    pay = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    validable = models.BooleanField(default=False)
    paspaye = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nom
```
order_file 오브젝트를 작성해, 고객이 주문서를 업로드하면 upload 폴더로 가게 했습니다.

파일업로드 view
<br />MyLoginRequiredMixin과 BaseCreateView를 상속받아 뷰를 작성했습니다.
```commandline
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
```
고객이 주문을 완료하면 자동으로 10개의 무작위 숫자를 발급해주는 random_letters 함수를 정의하고 사용하였습니다.
```commandline
def random_letters(digit):
     string_pool = string.digits
     result = ""
     for i in range(int(digit)):
         result += choice(string_pool)
     return result
```
주문완료시 자동으로 주문접수 이메일도 발송하게 하였습니다.

고객들이 주문완료한 주문리스트들을 보여주기 위한 리스트뷰를 작성하였습니다.
```commandline
class ApiCommandeListView(MyLoginRequiredMixin, BaseListView):
    def get_queryset(self):
        qs = Order.objects.filter(user__email=self.request.user.email).order_by('-create_dt')
        return qs
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_order(obj) for obj in qs]
        return JsonResponse(data=postList, safe=False, status=200)
```
다른 고객의 주문리스트는 볼 수 없도록 설정했습니다.

관리자 계정은 모든 고객의 주문리스트를 볼 수 있습니다.
```commandline
class ApiAdminListView( AdminOnlyMixin, BaseListView ):
    def get_queryset(self):
        if self.request.user.email == 'contact@salaisonsdelabreche.com':
            qs = Order.objects.all().order_by('-create_dt')
        else:
            qs = []
        return qs
```
AdminOnlyMixin을 상속받았는데, 이 mixin은 주문리스트를 부를때 로그인 되어있는 계정이 관리자 계정이 아니면 에러를 일으킵니다.
```commandline
class AdminOnlyMixin(LoginRequiredMixin, AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.email != 'contact@salaisonsdelabreche.com':
            data = {'message': "Vous n'avez pas droit"}
            return JsonResponse(data=data, safe=True, status=401)
        return super().dispatch(request, *args, **kwargs)
```

---
#### 주문 삭제
주문 삭제 view
```commandline
class ApiDeleteView(BaseDeleteView, OwnerOnlyMixin):
    model = Order
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        os.remove(self.object.order_file.path)
        self.object.delete()
        return JsonResponse(data={}, safe=True, status=204)
```
BaseDeleteView와 OwnerOnlyMixin을 상속받았습니다.
<br />OwnerOnlyMixin은 AccessMixin을 상속받아 본인 계정과 관리자 계정만 view를 실행시킬 수 있게 합니다.
```commandline
class OwnerOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.email != self.object.user.email and request.user.email != 'contact@salaisonsdelabreche.com':
            data = {'message': "Vous n'avez pas droit"}
            return JsonResponse(data=data, safe=True, status=403)
        return super().dispatch(request, *args, **kwargs)
```

---