from django.urls import path
from .views import *



urlpatterns = [
    path('',homeView, name="home"),
    path('login/', loginView, name="login"),
    path('register/', registerView, name="register"),
    path('logout/', logoutView, name="logout"),
    path('perfil/', perfilView, name="perfil"),
    path('uploadFile/', uploadFileView, name="uploadFile"),
    path('diagnostics/', diagnosticsView, name="diagnostics"),
    path('diagnostics/search/', search_results, name="search"),
    path('diagnostics/api/search_diagnostic/', DiagnosticsView.as_view()),
    path('centers/api/search_center/', CenterView.as_view()),
    path('centers/', centersView, name="centers"),
    path('diagnostic/<str:cod_diagnostic>', diagnosticView,name="diagnostic"),
]