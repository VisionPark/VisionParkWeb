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
from VisionParkWeb.forms import SetupParkingForm
from manageParking.models import Parking, Space
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render, reverse
import simplejson as json

def home(request):

    return render(request, 'home.html')

def about(request):

    return render(request, 'about.html')

def parkings(request):
    parkings = Parking.objects.all()
    parkingsJson =  json.dumps(list( parkings.values('id', 'lat', 'lon')))
    
    # Row selected  
    if request.method=="POST" and request.POST.get('idParkingSelected'):
        selectedParking = Parking.objects.get(id=request.POST.get('idParkingSelected'))
        
        zoom = request.POST.get('zoom')
        if selectedParking.num_spaces > 0:
            per_occupied = round(selectedParking.num_spaces_not_vacant/selectedParking.num_spaces *100)
        else:
            per_occupied = 0
        
        num_spaces = selectedParking.num_spaces
        num_spaces_vacant = selectedParking.num_spaces_vacant
        num_spaces_not_vacant = selectedParking.num_spaces_not_vacant
        num_spaces_unknown = selectedParking.num_spaces_unknown

        return render(request, 'parkings.html', {'parkings': parkings, 'parkingsJson':parkingsJson,
            'selectedParking':selectedParking, 'zoom':zoom, 'per_occupied':per_occupied,
            'num_spaces':num_spaces, 'num_spaces_vacant':num_spaces_vacant,
            'num_spaces_not_vacant':num_spaces_not_vacant, 'num_spaces_unknown':num_spaces_unknown
            })
            
    
    # First time or Close card button pressed
    # All parkings stats
    all_parkings = Parking.objects.all()
    num_spaces = len(all_parkings)
    num_spaces_vacant = 0
    num_spaces_not_vacant = 0
    num_spaces_unknown = 0

    for p in all_parkings:
        num_spaces_vacant += p.num_spaces_vacant
        num_spaces_not_vacant += p.num_spaces_not_vacant
        num_spaces_unknown += p.num_spaces_unknown

    return render(request, 'parkings.html', 
        {'parkings': parkings, 'parkingsJson': parkingsJson,
            'num_spaces':num_spaces, 'num_spaces_vacant':num_spaces_vacant,
            'num_spaces_not_vacant':num_spaces_not_vacant, 'num_spaces_unknown':num_spaces_unknown})

@login_required
def add_parking(request, id=None):
# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://stackoverflow.com/questions/1854237/django-edit-form-based-on-add-form

    # Once submitted the form
    if request.method=="POST": 

        hidden_id = request.POST.get('hidden_id')
        print("HIDDEN< ", hidden_id)

        # Editing existing parking
        if hidden_id is not None and hidden_id != 'None': 
            parking = get_object_or_404(Parking, pk=int(hidden_id))
            if parking.user != request.user:
                return HttpResponseForbidden()
        
            form = AddParkingForm(request.POST or None, instance=parking)
        
        # Creating new parking
        else:
            form = AddParkingForm(request.POST)
        
        # Valid data
        if form.is_valid():
            
            print("Valid form ->", form.cleaned_data)

            # Add the user and commit the object to database
            stock = form.save(commit=False)
            print("stock",stock)
            stock.user = request.user
            
            # Editing existing parking
            if hidden_id is not None and hidden_id != 'None': 
                # Prevent the canvas from being removed
                stock.save(update_fields=['name', 'address', 'postcode', 'lon', 'lat', 'date_modified', 'img'])
            # Creating new parking
            else:
                 stock.save()


            parkings = Parking.objects.filter(user=request.user)
            return redirect('/manage/myparkings', {'parkings' : parkings, 'added_ok': True})
            
        # Invalid data
        else:
            print(form.errors)

    # First time entering the page
    else:
        # Editing existing parking
        if id:
            print("ID: ", id)
            parking = get_object_or_404(Parking, pk=id)
            if parking.user != request.user:
                return HttpResponseForbidden()
        
            form = AddParkingForm(request.POST or None, instance=parking)

        # Creating new parking
        else:
            form = AddParkingForm()
        
    return render(request, "manage/add.html", {'form' : form})

@login_required
def setup_parking(request, id=None):
# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://stackoverflow.com/questions/1854237/django-edit-form-based-on-add-form

    # Once submitted the form
    if request.method=="POST": 

        vertex = request.POST.get('vertex')
        print("ID< ", id)

        # Setup existing parking
        if id is not None and id != 'None' and vertex is not None and vertex != 'None': 
            parking = get_object_or_404(Parking, pk=int(id))
            if parking.user != request.user:
                return HttpResponseForbidden()
        
            # Save canvas config to parking entry in DB
            parking.canvas = request.POST.get('canvas')
            parking.save()
            
            # Remove previous spaces from the parking
            Space.objects.filter(parking=parking).delete()

            # Add the just created spaces from the canvas
            vertex =  json.loads(vertex) # Parse the stringyfied JSON
            
            new_spaces = []
            for i,v in enumerate(vertex): #For each set of vertex of the spaces setup
            # https://www.youtube.com/watch?v=DgokREtOaVA
                print(i,":", v)
                space = Space(
                    parking = parking,
                    shortName = "A"+str(i),
                    vertex = v,
                )
                new_spaces.append(space)
            Space.objects.bulk_create(new_spaces)

            parkings = Parking.objects.filter(user=request.user)
            parkingImg = parking.img
            return redirect('/manage/myparkings', {'parkings' : parkings, 'added_ok': True})

        # Creating new parking, redirect
        else:
            parkings = Parking.objects.filter(user=request.user)
            return redirect('/manage/myparkings', {'parkings' : parkings, 'setup_ok': False, 'parkingImg': parkingImg})

    # First time entering the page
    else:
        # Editing existing parking
        if id:
            print("ID: ", id)
            parking = get_object_or_404(Parking, pk=id)
            if parking.user != request.user:
                return HttpResponseForbidden()

            # spaces = get_list_or_404(Space, parking=parking)      
            canvas = parking.canvas
            parkingImg = parking.img
            return render(request, "manage/setup.html", {'canvas' : canvas, 'parkingImg': parkingImg})

        # Creating new parking
        else:
            parkings = Parking.objects.filter(user=request.user)
            return redirect('/manage/myparkings', {'parkings' : parkings, 'setup_ok': False})
        
@login_required   
def my_parkings(request):
  # https://stackoverflow.com/questions/59408167/list-of-current-user-objects-in-django-listview

    if request.method=="POST":
        return redirect("/manage/delete/"+request.POST.get('hidden_id'))

    parkings = Parking.objects.filter(user=request.user)

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
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required 
def parking_delete(request, id):
 # https://www.youtube.com/watch?v=3VBHWLFza4s

    parking = get_object_or_404(Parking, id=id)

    if parking.user != request.user:
        return HttpResponseForbidden()

    else:
        print("Deleted: ", parking)
        parking.delete()
         
    parkings = Parking.objects.filter(user=request.user)
    return redirect('/manage/myparkings', {'parkings' : parkings, 'deleted_ok': parking})