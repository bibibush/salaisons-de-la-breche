from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
   path('login/', views.ApiLoginView.as_view(), name='login'),
   path('getme/', views.GetMe.as_view(), name='getme'),
   path('logout/', views.ApiLogoutView.as_view(), name='logout'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('pwdchange/', views.ApipwdChangeView.as_view(), name='pwdchange'),
   path('download/', views.ApiFileDownloadView.as_view(), name='download'),
   path('upload/', views.ApiFileUploadView.as_view(), name='upload'),
   path('success/<int:pk>/', views.ApiCommandeInfoView.as_view(), name='success'),
   path('excel/<int:pk>/', views.ApiCommandExcelView.as_view(), name='excel'),
   path('list/', views.ApiCommandeListView.as_view(), name='list'),
   path('info/<int:pk>/update', views.ApiInfoUpdateView.as_view(), name='info_update'),
   path('excel/<int:pk>/update', views.ApiExcelUpdateView.as_view(), name='excel_update'),
   path('date/<int:pk>/update', views.ApiDateUpdateView.as_view(), name='date_update')
]