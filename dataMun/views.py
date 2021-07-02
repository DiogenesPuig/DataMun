from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .script import *
from .filters import *
from django.conf import settings

from django.forms.utils import ErrorList
import datetime

from rest_framework import generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *


# Create your views here.


@login_required()
def perfilView(request):
    return render(request, "perfil.html")


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")


@unauthenticated_user
def loginView(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Exitoso")
            try:
                return redirect(request.POST.get('next'))
            except:
                return redirect('home')
        else:
            messages.error(request, "Usuario o Contraseña Incorrecta")

            return render(request, 'login.html', context)

    return render(request, 'login.html', context)


@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Account was created for " + username)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def homeView(request):
    context = {

    }
    return render(request, 'home.html', )


class PaceintePorDiagnostico():
    def __init__(self, cantPacientePorDiagnostico, diagnostico):
        self.cantPacientePorDiagnostico = cantPacientePorDiagnostico
        self.diagnostico = diagnostico


@user_passes_test(lambda u: u.is_staff)
def diagnosticsView(request):
    try:

        year = datetime.datetime.now().year

        weeks = Week.objects.filter(year=year)
        max_week = weeks[0]
        for week in weeks:
            if week.week > max_week.week:
                max_week = week

        diagnostics = Diagnostic.objects.all()
        diagnostic_cases = DiagnosticCases.objects.all()
        alerts = []
        diagn_cod = []

        for diagnostic in diagnostics:
            if len(alerts) != 100:
                dots = GetAlert(diagnostic_cases, diagnostic, max_week, year)
                if dots.cases >= dots.top_rank and dots.cases != 0 and dots.week == max_week.week:
                    if diagnostic.code not in diagn_cod:
                        alerts.append({'diagnostic': diagnostic, 'cases': dots.cases})
                        diagn_cod.append(diagnostic.code)
            else:
                break

        context = {
            'max_week': max_week,
            'alerts': alerts,
        }
    except:
        context = {}
    return render(request, 'diagnostics.html', context)


@user_passes_test(lambda u: u.is_staff)
def diagnosticView(request, cod_diagnostic):
    try:
        diagnostic = Diagnostic.objects.get(code=cod_diagnostic)
        diagnostic_cases = DiagnosticCases.objects.filter(diagnostic=diagnostic)

        weeks = Week.objects.all()
        p = DiagnosticCasesFilter(request.GET, queryset=diagnostic_cases)

        if request.GET:
            messages.info(request, "Filters aplied")
        try:
            year = int(request.GET.get('year__lt'))
        except:
            year = 0
        if year == 0:
            year = 2021

        centrosName = []
        centros = []
        centro = ""
        suma = 0
        pacientes = p.qs.filter(diagnostic=diagnostic).order_by("center")
        for pac in pacientes:
            if pac.center not in centrosName:
                if pac.center.name == centro:
                    suma += pac.cases
                else:

                    centrosName.append(centro)
                    n = 'centro ' + centro
                    co = {
                        'nombre': n,
                        'cases': suma,
                        'cod': pac.center.code,
                    }

                    centros.append(co)

                    centro = pac.center.name

                    suma = 0
            if len(centrosName) >= 20:
                break

        averages, cumulative = GetGraphicAverages(p.qs, diagnostic, weeks, year, 3)
        print('graphic 1 and 3 Ok')
        quartiles = GetGraphicQuartiles(p.qs, diagnostic, weeks, year, 3)
        print('graphic 2 Ok')
        context = {
            'averages': averages,
            'quartiles': quartiles,
            'cumulative': cumulative,
            'diagnostic': diagnostic,
            'filterP': p,
            'google_api_key': settings.APY_KEY,
            'centros': centros,
        }
    except:
        context = {}
    return render(request, 'diagnostic.html', context)


@user_passes_test(lambda u: u.is_staff)
def uploadFileView(request):
    form = CreateFileForm()
    if request.method == "POST":  # If the form has been submitted...

        # All validation rules pass
        form = CreateFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            file = SpreadSheet.objects.get(pk=file.id)
            success = insertWorkbook(file)

            """
            if len(success) != 1:
                file = SpreadSheet.objects.get(pk=file.id)
                file.delete()
                for error in success:
                    if error[0] == 1:
                        form._errors["tabla"] = ErrorList([u" El archivo subido debe ser excel."])
                    if error[0] == 2:

                        form._errors["tabla"] = ErrorList([u" Revisa que el titulo de la hoja este correcto con su año y semana"])

                    context = {
                        'form':form
                    }

                return render(request, 'uploadFile.html',context)"""
            messages.success(request, "El archivo " + str(file.file) + ' fue agregado')
            return redirect('diagnostics')  ## redirects to aliquot page ordered by the most recent



    else:
        form = CreateFileForm()  # An unbound form

    context = {
        'form': form
    }
    return render(request, 'uploadFile.html', context)


def centersView(request):
    return render(request, 'centers.html')


# django rest_fremework views
class CenterView(generics.ListAPIView):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = {'name': ['icontains']}


class DiagnosticsView(generics.ListAPIView):
    queryset = Diagnostic.objects.all()
    serializer_class = DiagnosticSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = {'name': ['icontains']}

