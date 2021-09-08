
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'diagnostics', DiagnosticReadonlyViewSet)
router.register(r'centers', CenterReadonlyViewSet)



urlpatterns = [
    path('',homeView, name="home"),

    path('login/', loginView, name="login"),
    path('register/', registerView, name="register"),
    path('logout/', logoutView, name="logout"),
    path('perfil/', perfilView, name="perfil"),

    path('uploadFile/', uploadFileView, name="uploadFile"),

    path('diagnostics/', diagnosticsView, name="diagnostics"),
    path('diagnostics/<str:cod_diagnostic>', diagnosticView,name="diagnostic"),

    path('centers/', centersView, name="centers"),
    path('centers/<int:cod_center>', centerView, name="center"),
    
    path('api/', include(router.urls)),
]