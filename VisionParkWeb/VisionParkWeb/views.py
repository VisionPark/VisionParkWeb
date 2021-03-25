from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

    return render(request, "manage/setup.html")

@login_required   
def my_parkings(request):

    return render(request, "manage/myparkings.html")



