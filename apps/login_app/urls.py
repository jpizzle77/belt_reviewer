from django.conf.urls import url
from . import views           # This line is new!

app_name = "login_app"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^(?P<number>\d+)$', views.user, name="user"),
  
   
    ]