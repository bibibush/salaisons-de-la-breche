from django.urls import path
from django.views.generic import TemplateView

from api import views

app_name = 'api'
urlpatterns = [
   path('load/', views.ApiView.as_view(), name='load'),
   path('login/', views.ApiLoginView.as_view(), name='login'),
   path('getme/', views.GetMe.as_view(), name='getme'),
   path('logout/', views.ApiLogoutView.as_view(), name='logout'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('pwdchange/', views.ApipwdChangeView.as_view(), name='pwdchange'),
   path('download/', views.ApiFileDownloadView.as_view(), name='download'),
   path('bondownload/', views.ApiBonDownloadView.as_view(), name='bondownload'),
   path('upload/', views.ApiFileUploadView.as_view(), name='upload'),
   path('success/<int:pk>/', views.ApiCommandeInfoView.as_view(), name='success'),
   path('manage/<int:pk>/',views.ApiCommandeManageView.as_view(),name='manage'),
   path('ad/manage/<int:pk>/',views.ApiAdminCommandeManageView.as_view(),name='ad_manage'),
   path('excel/<int:pk>/', views.ApiCommandExcelView.as_view(), name='excel'),
   path('list/', views.ApiCommandeListView.as_view(), name='list'),
   path('ad/list/', views.ApiAdminListView.as_view(), name='ad_list'),
   path('info/<int:pk>/update', views.ApiInfoUpdateView.as_view(), name='info_update'),
   path('excel/<int:pk>/update', views.ApiExcelUpdateView.as_view(), name='excel_update'),
   path('date/<int:pk>/update', views.ApiDateUpdateView.as_view(), name='date_update'),
   path('pay/<int:pk>/update', views.ApiPayUpdateView.as_view(), name='pay_update'),
   path('commande/<int:pk>/delete', views.ApiDeleteView.as_view(), name='delete'),
]