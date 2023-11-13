from django.urls import path
from django.views.generic import TemplateView

from users import views

app_name = 'users'
urlpatterns = [
  path('<int:pk>/infoupdate/', views.UserInfoUpdate.as_view(), name='userinfoupdate'),
]