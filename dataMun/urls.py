from django.urls import path
from .views import *

urlpatterns = [
    path('',homeView, name="home"),
    path('login/', loginView, name="login"),
    path('register/', registerView, name="register"),
    path('logout/', logoutView, name="logout"),
    path('perfil/', perfilView, name="perfil"),
    path('uploadFile/', uploadFileView, name="uploadFile"),
]