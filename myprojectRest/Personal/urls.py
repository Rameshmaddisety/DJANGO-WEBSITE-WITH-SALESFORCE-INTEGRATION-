from django.urls import path
from . import views

# from .views import create_salesforce_account
urlpatterns = [

    path('', views.index, name='index'),
     
    path("login",views.login, name="login"),
    path("logout",views.logout,name="logout"),
    path("register", views.register, name="register"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("forget",views.forget,name="forget"),
    path("UpdateOTP",views.UpdateOTP,name="UpdateOTP")
    
]