from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from VisionParkWeb.forms import SignUpForm
from VisionParkWeb.forms import AddParkingForm
from manageParking.models import Parking

def home(request):

    return render(request, 'home.html')


def about(request):

    return render(request, 'about.html')


def home2(request):

    nombre = "Victor"
    apellido = "RN"

    #doc_externo = open('E:/OneDrive - UNIVERSIDAD DE HUELVA/TFG/VisionParkWeb-main/VisionParkWeb/VisionParkWeb/VisionParkWeb/templates/plantillaPrueba.html')
    #template = Template(doc_externo.read())
    #doc_externo.close()

    #doc_externo = get_template('plantillaPrueba.html')


    ctx = {"nombre_persona" : nombre, 
        "apellido_persona" : apellido, 
        "year":datetime.datetime.now().year, 
        "temas":["hola", "buenas", "tardes", "crack"]}

    #documento = doc_externo.render(ctx)

    #fecha_actual = datetime.datetime.now()

    return render(request, 'plantillaPrueba.html', ctx)

def calculaEdad(request, edad, year):

    periodo = year - datetime.datetime.now().year
    edadFutura = edad + periodo

    
    documento = f"""<html><body>
    <h2>En el año {year} tendrás {edadFutura} años</h2>

    </body></html>
    """

    return HttpResponse(documento)


def hereda(request):

    fecha = datetime.datetime.now()

    return render(request, 'hereda.html', {"dame_fecha": fecha})

@login_required
def setup(request):
# https://docs.djangoproject.com/en/3.2/topics/forms/
    if request.method=="POST":
        print(request.POST)
        form = AddParkingForm(request.POST)
        
        if form.is_valid():
            
            print("Valid form ->", form.cleaned_data)

            # Add the user and commit the object to database
            stock = form.save(commit=False)
            print("stock",stock)
            stock.user = request.user
            stock.save()
            return render(request, "manage/myparkings.html")
        else:
            print(form.errors)
    else:
        form = AddParkingForm()

    return render(request, "manage/setup.html", {'form' : form})

@login_required   
def my_parkings(request):
  # https://stackoverflow.com/questions/59408167/list-of-current-user-objects-in-django-listview
    model = Parking

    parkings = Parking.objects.filter(
            user=request.user
        )

    return render(request, "manage/myparkings.html", {'parkings' : parkings})

# TODO: keep data on submit with errors
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})