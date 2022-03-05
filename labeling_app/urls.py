from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('confirm', views.confirm_name, name='confirm'),
    path('welcome', views.welcome, name='welcome'),
    path('label', views.labelling, name='label'),
    path('done', views.done, name='done'),
]