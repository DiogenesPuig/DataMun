# django imports
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect

# django-rest-framework imports
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# my imports
from .decorators import unauthenticated_user
from .forms import CreateUserForm, CreateFileForm, CenterForm, DiagnosticForm
from .script import GetAlert, GetGraphicAverages, GetGraphicQuartiles, insertWorkbook
from .filters import DiagnosticCasesFilter,WeekFilter
from .serializers import CenterSerializer, DiagnosticSerializer
from .models import ApiKey, Center, Diagnostic, DiagnosticCases, SpreadSheet, Week, Year
import datetime


# Create your views here.
def helpView(request):
    context = {

    }
    return render(request, 'help.html', )

@login_required()
def perfilView(request):
    """This view function is used to render profile"""
    return render(request, "perfil.html")


def logoutView(request):
    """This view function is used to redirect to home when you
    logout """
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")

@unauthenticated_user
def loginView(request):
    """This view function is used to login in the page"""
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
    """This view function is used to create a new profile"""
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Cuenta creada para " + username)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def helpView(request):
    """This view function render Home"""
    context = {

    }
    return render(request, 'help.html', )


class PaceintePorDiagnostico():
    def __init__(self, cantPacientePorDiagnostico, diagnostico):
        self.cantPacientePorDiagnostico = cantPacientePorDiagnostico
        self.diagnostico = diagnostico

@user_passes_test(lambda u: u.is_staff)
def diagnosticsView(request):
    """
    This view function show us all the diagnostics and alerts(if it exists)
    """
    try:
        year = datetime.datetime.now().year
        year_obj = Year.objects.get(year=year)
    except:
        year_obj = Year.objects.last()

    weeks = Week.objects.filter(year=year_obj).order_by('-week')
    try:
        max_week = weeks[0]
        max_week = Week.objects.get(pk=max_week.id)
        print(max_week.week)
        """for week in weeks:
            if week.week > max_week.week:
                max_week = week"""

        diagnostics = Diagnostic.objects.all()
        diagnostic_cases = DiagnosticCases.objects.all()
        alerts = []
        diagn_cod = []

        for diagnostic in diagnostics:
            if ( diagnostic.alert):
                if len(alerts) != 10:
                    dots = GetAlert(diagnostic_cases, diagnostic, max_week, year)
                    if dots.cases > dots.top_rank and dots.cases != 0 and dots.week == max_week.week:
                        if diagnostic.code not in diagn_cod:
                            alerts.append({'diagnostic': diagnostic, 'cases': dots.cases})
                            diagn_cod.append(diagnostic.code)
                else:
                    break
            

        context = {
            'max_week': max_week,
            'alerts': alerts,
        }
        
            
        return render(request, 'diagnostics.html', context)
    except:
        messages.info(request, "No hay diagnosticos cargados")
        return redirect('uploadFile')

@user_passes_test(lambda u: u.is_staff)
def diagnosticView(request, cod_diagnostic):
    """
    This view function show us the information of each diagnostic with
    his own charts and it have filters if you need to use
    """
    diagnostic = Diagnostic.objects.get(code=cod_diagnostic)
    diagnostic_form = DiagnosticForm(instance=diagnostic)
    if request.method == "POST":  # If the form has been submitted...

        # All validation rules pass
        diagnostic_form = DiagnosticForm(request.POST,instance=diagnostic)
        if diagnostic_form.is_valid():
            diagnostic = diagnostic_form.save()
            messages.success(request, "El diagnostico " + str(diagnostic.name) + ' fue editado ')
              ## redirects to aliquot page ordered by the most recent

    diagnostic_cases = DiagnosticCases.objects.filter(diagnostic=diagnostic)

    weeks = Week.objects.all()
    p = DiagnosticCasesFilter(request.GET, queryset=diagnostic_cases)
    w = WeekFilter(request.GET)
    num_years = 3
    if request.GET:
        messages.success(request, "Filtros aplicados correctamente")
        try:
            year = Year.objects.get(pk=request.GET.get('year')).year
        except:
            year = Year.objects.all().order_by('-year')[0].year
        try:
            num_years = int(request.GET.get('num_years'))
        except:
            num_years = 3
    else:
        year = Year.objects.all().order_by('-year')[0].year

    pacientes = p.qs.filter(diagnostic=diagnostic).order_by("center")


    centers = []
    centers_obj = Center.objects.all()
    for center in centers_obj:
        if center.longitude is None:
            center.longitude = 0.1

        if center.latitude is None:
            center.latitude = 0.1
        n = 'centro ' + center.name
        c = {
            'nombre': n,
            'cases': center.get_cases(diagnostic),
            'code': center.code,
            'lat': center.latitude,
            'lon': center.longitude
        }
        centers.append(c)

    averages, cumulative_averages = GetGraphicAverages(p.qs, diagnostic, weeks, year, num_years)
    print('graphic 1 and 3 Ok')
    quartiles, cumulative_quartiles = GetGraphicQuartiles(p.qs, diagnostic, weeks, year, num_years)
    print('graphic 2 Ok')
    try: 
        API = ApiKey.objects.first().key
    except:
        API = ""
        messages.warning(request,"No se encontro una KEY de GOOGLE MAPS, debe agregar una valida desde admin")

    context = {
        'diagnostic_form':diagnostic_form,
        'averages': averages,
        'quartiles': quartiles,
        'cumulative_averages': cumulative_averages,
        'cumulative_quartiles': cumulative_quartiles,
        'diagnostic': diagnostic,
        'centers': centers,
        'year': year,
        'diagnostic_cases_filter': p,
        'week_filter':w,
        'num_years': num_years,
        'google_api_key': API,
        
    }

    #context = {}
    return render(request, 'diagnostic.html', context)

@user_passes_test(lambda u: u.is_staff)
def uploadFileView(request):
    """
    This view function is used to upload a xls file to later
    read and process the data in order to load the information to the
    database
    """
    form = CreateFileForm()
    if request.method == "POST":  # If the form has been submitted...

        # All validation rules pass
        form = CreateFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = SpreadSheet(file=request.FILES['file'])
            
            
            try:
                success = insertWorkbook(file)
            except:

                messages.error(request, "Error formato de hoja de calculos incorrecto.")
                return redirect("uploadFile")
            file = form.save()
            file = SpreadSheet.objects.get(pk=file.id)
            messages.success(request, "El archivo " + str(file.file) + ' fue agregado exitosamente')
            messages.success(request, success)
            return redirect('diagnostics')  ## redirects to aliquot page ordered by the most recent
    else:
        form = CreateFileForm()  # An unbound form

    context = {
        'form': form
    }
    return render(request, 'uploadFile.html', context)

@user_passes_test(lambda u: u.is_staff)
def centersView(request):
    """This view function is empty(for now)"""
    return render(request, 'centers.html')

@user_passes_test(lambda u: u.is_staff)
def centerView(request, cod_center):
    center = Center.objects.get(code=cod_center)
    center_form = CenterForm(instance=center)
    if request.method == "POST":  # If the form has been submitted...

        # All validation rules pass
        center_form = CenterForm(request.POST,instance=center)
        if center_form.is_valid():
            center = center_form.save()
            messages.success(request, "El centro " + str(center.name) + ' fue editado ')
            return redirect('centers')  ## redirects to aliquot page ordered by the most recent
    else:
        center_form = CenterForm(instance=center) # An unbound form
    
    try: 
        API = ApiKey.objects.first().key
    except:
        API = ""
        messages.warning(request,"No se encontro una KEY de GOOGLE MAPS, debe agregar una valida desde admin")

    context = {
        'center': center,
        'center_form':center_form,
        'google_api_key': API,

    }

    #context = {}
    return render(request, 'center.html', context)


# django rest_fremework views

class CenterReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Center.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = CenterSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = {'name': ['icontains']}


class DiagnosticReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Diagnostic.objects.all().order_by('code')
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = DiagnosticSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = {'name': ['icontains']}

