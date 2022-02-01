from dataclasses import field, fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from .models import Doctormodel,Patientmodel,Appointmentmodel



class Adminsignupform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {'password':forms.PasswordInput()}

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {'password':forms.PasswordInput()}
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model  =  Doctormodel
        fields = ['address','mobile','department','status','profile_pic']
        
        
        
class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {'password':forms.PasswordInput()}
        
class PatientForm(forms.ModelForm):
    assignedDoctorId = forms.ModelChoiceField(queryset=Doctormodel.objects.all().filter(status=True),empty_label="Doctor Name and Department",to_field_name="user_id")
    
    class Meta:
        model  =  Patientmodel
        fields = ['address','mobile','symptoms','status','profile_pic']
        
        
        
class ApointmentsForm(forms.ModelForm):
    patientId = forms.ModelChoiceField(queryset = Patientmodel.objects.all().filter(status = True),empty_label="Name and Symtomps",to_field_name="user_id")
    doctorId = forms.ModelChoiceField(queryset = Doctormodel.objects.all().filter(status = True),empty_label="Doctor Name and Department",to_field_name="user_id")
    class Meta:
        model  =  Appointmentmodel
        fields = ['description','status']
        
        
class PatientRequestForAppointment(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset = Doctormodel.objects.all().filter(status = True),empty_label = "Doctor Name And Department",to_field_name="user_id")
    class Meta:
        model = Appointmentmodel
        fields = ['description','status']            