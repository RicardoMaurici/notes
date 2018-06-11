from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout_user'),
    path('mynotes/', views.mynotes, name='mynotes'),
    path('newnote/', views.newnote, name='newnote'),
    path('edit/<note>', views.edit, name='edit'),
    path('edit/', views.edit, name='edit'),
]
