from django.conf.urls import url
from . import views           # This line is new!

app_name = "book_app"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add$', views.add, name="add"),
    
    url(r'^(?P<number>\d+)$', views.show, name="show"),
    url(r'^review$', views.review, name="review"),
   
    url(r'^clear$', views.clear, name="clear"),
   
    ]