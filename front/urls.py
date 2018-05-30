from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^aaa$', views.view_a, name='view_a'),
    url('register/', views.register, name='register'),
    url('login_check/', views.login_check, name='login_check')

]
