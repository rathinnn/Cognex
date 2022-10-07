from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from .models import Project, Task
class DatePickerInput(forms.DateInput):
    input_type = 'date'
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'startDate', 'expectedDate')
        widgets = {
            'title' : forms.TextInput(attrs={'class': "form-control"}),
            'description' : forms.Textarea(attrs={'class': "form-control"}),
            'startDate' : DatePickerInput(attrs={'class': "form-control"}),
            'expectedDate' : DatePickerInput(attrs={'class': "form-control"})
        }

class TaskForm(forms.ModelForm):
    Assigned = forms.CharField(max_length=100)
    class Meta:
        model = Task
        fields = ('title', 'description', 'startDate', 'expectedDate', 'weight', 'Type')
        widgets = {
            'title' : forms.TextInput(attrs={'class': "form-control"}),
            'description' : forms.Textarea(attrs={'class': "form-control"}),
            'startDate' : DatePickerInput(attrs={'class': "form-control"}),
            'expectedDate' : DatePickerInput(attrs={'class': "form-control"}),
            'weight' : forms.NumberInput(attrs={'class': "form-control"}),
            'Type' : forms.Select(attrs={'class': "form-control"}),
            'Assigned' : forms.TextInput(attrs={'class': "form-control"})
        }
        

