from manageParking.models import Space
from manageParking.models import Parking
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Required. Name')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2')

class AddParkingForm(ModelForm):
    class Meta:
        model = Parking
        exclude = ('user', 'date_created', 'date_modified')

class SetupParkingForm(ModelForm):
    class Meta:
        model = Space
        fields = '__all__'