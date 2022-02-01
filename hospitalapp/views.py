from unicodedata import name
from django.shortcuts import redirect, render,HttpResponseRedirect
from httpx import request
from .models import Doctormodel,Patientmodel,Appointmentmodel
from .forms import DoctorUserForm,DoctorForm,PatientUserForm,PatientForm,ApointmentsForm,Adminsignupform,PatientRequestForAppointment
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
# Create your views here.



## <===== HOME PAGE VIEWS ===>

def home(request):
    return render(request,"index.html")
def admin_sign_up(request):
    userform = Adminsignupform()
    if request.method == "POST":
        userform = Adminsignupform(request.POST)
        if userform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            my_groups = Group.objects.get_or_create(name = "ADMIN")
            my_groups[0].user_set.add(user)
            return HttpResponseRedirect("adminlogin")
    return render(request,"adminsignup.html",{"userform":userform})    
def doctor_sign_up(request):
    userform = DoctorUserForm()
    doctorform = DoctorForm()
    if request.method == 'POST':
        userform = DoctorUserForm(request.POST)
        doctorform = DoctorForm(request.POST, request.FILES)
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.save()
            my_groups = Group.objects.get_or_create(name = "DOCTOR")
            my_groups[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')    
    return render(request,'doctor_sign_up.html',{'userform':userform,'doctorform':doctorform})

def patient_sign_up(request):
    userform=PatientUserForm()
    patientform=PatientForm()
    
    if request.method=='POST':
        userform=PatientUserForm(request.POST)
        patientform=PatientForm(request.POST,request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user=userform.save()
            user.set_password(user.password)
            user.save()
            patient=patientform.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            my_patient_group = Group.objects.get_or_create(name = "PATIENT")
            my_patient_group[0].user_set.add(user)
            return HttpResponseRedirect("patientlogin")
    return render(request,'patient_sign_up.html',{'userform':userform,'patientform':patientform})    


def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()
def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()
def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()
##<========= check whether user is admin,doctor or patient ==============>
def afterlogin_redirect(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_doctor(request.user):
        approveddoctor = Doctormodel.objects.all().filter(user_id = request.user.id,status = True)
        if approveddoctor:
            return redirect("doctor_dashboard")
        else:
            return render(request,"doctor_wait_for_approvel.html")
    elif is_patient(request.user):
        approvedpatient = Patientmodel.objects.all().filter(user_id = request.user.id,status = True)
        if approvedpatient:
            return redirect("patient_dashboard")
        else:
            return render(request,"patient_wait_for_approvel.html")
        
    
            




## <===========  Admin Related views =============>
@login_required(login_url="adminlogin")
def admin_dashboardviews(request):
    doctor = Doctormodel.objects.all().order_by("id")
    patient = Patientmodel.objects.all().order_by("id")
    appointment = Appointmentmodel.objects.all().order_by("id")
    doctorcount =  Doctormodel.objects.all().filter(status = True).count()
    pendingdoctor = Doctormodel.objects.all().filter(status = False).count()
    patientcount = Patientmodel.objects.all().filter(status = True).count()
    pendingpatient = Patientmodel.objects.all().filter(status = False).count()
    appointmentcount = Appointmentmodel.objects.all().filter(status = True).count()
    pendingappointment = Appointmentmodel.objects.all().filter(status = False).count()
    return render(request, "admin_dashboard.html",{'doctor':doctor,'patient':patient,'appointment':appointment,'doctorcount':doctorcount,'pendingdoctor':pendingdoctor,'patientcount':patientcount,'pendingpatient':pendingpatient,'appointmentcount':appointmentcount,'pendingappointment':pendingappointment})


def admin_view_approved_doctor_records(request):
    approved_doctors = Doctormodel.objects.all().filter(status = True)
    return render(request,'Admin_view_Approved_Doctor_Records.html',{'approved_doctors':approved_doctors})

def admin_add_doctors(request):
    userform = DoctorUserForm()
    doctorform = DoctorForm()
    if request.method == 'POST':
        userform = DoctorUserForm(request.POST)
        doctorform = DoctorForm(request.POST, request.FILES)
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()
            
            my_groups = Group.objects.get_or_create(name = "DOCTOR")
            my_groups[0].user_set.add(user)
            
        return HttpResponseRedirect('admin-view-approved-doctor-records')    
    return render(request,'admin_add_doctors.html',{'userform':userform,'doctorform':doctorform})

def admin_update_doctor_record(request,pk):
    doctor = Doctormodel.objects.get(id = pk)
    user = User.objects.get(id = doctor.user_id)
    userform = DoctorUserForm(instance=user)
    doctorform = DoctorForm(request.FILES,instance = doctor)
    if request.method == 'POST':
        userform = DoctorUserForm(request.POST,instance=user)
        doctorform = DoctorForm(request.POST, request.FILES,instance=doctor)
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()
            return redirect('admin-view-approved-doctor-records')    
    return render(request,'admin_update_doctors_records.html',{'userform':userform,'doctorform':doctorform})


def admin_delete_doctor_from_hospital(request,pk):
    doctor = Doctormodel.objects.get(id = pk)
    user = User.objects.get(id = doctor.user_id)
    doctor.delete()
    user.delete()
    return redirect("admin-view-approved-doctor-records")


def admin_view_pending_doctor_names(request):
    pending_doctors = Doctormodel.objects.all().filter(status = False)
    return render(request,'admin_view_all_pending_doctors.html',{"pending_doctors":pending_doctors})



def admin_add_patients(request):
    userform = PatientUserForm()
    patientform = PatientForm()
    if request.method == 'POST':
        userform = PatientUserForm(request.POST)
        patientform = PatientForm(request.POST, request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            
            my_groups = Group.objects.get_or_create(name="PATIENT")
            my_groups[0].user_set.add(user)
            
        return HttpResponseRedirect('admin_view_admitted_patients_records')    
    return render(request,'admin_add_patients.html',{'userform':userform,'patientform':patientform})

def admin_update_patients(request,pk):
    patient = Patientmodel.objects.get(id = pk)
    user = User.objects.get(id = patient.user_id)
    userform = PatientUserForm(instance=user)
    patientform = PatientForm(request.FILES,instance = patient)
    if request.method == 'POST':
        userform = PatientUserForm(request.POST,instance = user)
        patientform = PatientForm(request.POST, request.FILES,instance = patient)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            return redirect('admin_view_admitted_patients_records')    
    return render(request,'admin_update_patient.html',{'userform':userform,'patientform':patientform})

def admin_view_admitted_patients_records(request):
    admitted_patients = Patientmodel.objects.all().filter(status = True)
    return render(request,'admin_view_admitted_patients_records.html',{'admitted_patients':admitted_patients}) 

def admin_view_pending_patients_names(request):
    pending_patients = Patientmodel.objects.all().filter(status = False)
    return render(request,'admin_view_all_pending_patients.html',{"pending_patients":pending_patients})

def admin_view_all_appointments(request):
    appointments = Appointmentmodel.objects.all().filter(status = True)
    return render(request,'admin_view_all_appointments.html',{'appointments':appointments})

def admin_add_appointments(request):
    appointmentform = ApointmentsForm()
    if request.method == 'POST':
        appointmentform = ApointmentsForm(request.POST)
        if appointmentform.is_valid():   
            appoint = appointmentform.save(commit=False)
            appoint.patientId = request.POST.get("patientId")
            appoint.doctorId = request.POST.get("doctorId")
            appoint.patientName = User.objects.get(id = request.POST.get("patientId")).first_name
            appoint.doctorName = User.objects.get(id = request.POST.get("doctorId")).first_name
            appoint.status = True
            appoint.save()
        return HttpResponseRedirect('admin_view_all_appointments')
    return render(request,'admin_add_appointments.html',{'appointmentform':appointmentform})

def admin_view_pending_appointment(request):
    
    appointments=Appointmentmodel.objects.all().filter(status=False)
    return render(request,'admin_view_pending_appointment.html',{'appointments':appointments})

def admin_approved_the_pending_appointments(request,pk):
    appointments = Appointmentmodel.objects.get(id = pk)
    appointments.status = True
    appointments.save()
    return redirect("admin_view_all_appointments")

def admin_delete_pending_appointments(request,pk):
    appointmets = Appointmentmodel.objects.get(id = pk)
    appointmets.delete()
    return redirect("admin_view_pending_appointment")

def admin_delete_approved_appointments(request,pk):
    appointmets = Appointmentmodel.objects.get(id = pk)
    appointmets.delete()
    return redirect("admin_view_all_appointments")

def admin_approved_pending_patient(request,pk):
    patients = Patientmodel.objects.get(id = pk)
    print("=====================")
    print(pk)
    print("===================")
    patients.status = True
    patients.save()
    return redirect("admin_view_pending_patients_names")
    
def admin_delete_pending_patient(request,pk):
    patients = Patientmodel.objects.get(id = pk)
    user = User.objects.get(id = patients.user_id)
    patients.delete()
    user.delete()
    return redirect("admin_view_pending_patients_names")

def admin_delete_approved_patient(request,pk):
    patients = Patientmodel.objects.get(id = pk)
    user = User.objects.get(id = patients.user_id)
    patients.delete()
    user.delete()
    return redirect("admin_view_admitted_patients_records")

def admin_approved_pending_doctor(request,pk):
    doctor = Doctormodel.objects.get(id = pk)
    print("=====================")
    print(pk)
    print("===================")
    doctor.status = True
    doctor.save()
    return redirect("admin-view-approved-doctor-records")
    
def admin_delete_pending_doctor(request,pk):
    doctor = Doctormodel.objects.get(id = pk)
    user = User.objects.get(id = doctor.user_id)
    doctor.delete()
    user.delete()
    return redirect("admin-view-approved-doctor-records")







## <===========  Doctor Related views =============>
def doctor_dashboard(request):
    patientscount = Patientmodel.objects.all().filter(status = True, assignedDoctorId = request.user.id).count()
    appointmentscount = Appointmentmodel.objects.all().filter(status = True, doctorId = request.user.id).count()
    
    doctor_profile_pic = Doctormodel.objects.get(user_id = request.user.id)
    
    appointments = Appointmentmodel.objects.all().filter(status = True,doctorId = request.user.id).order_by("-id")
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = Patientmodel.objects.all().filter(status = True,user_id__in = patientid).order_by("-id")
    combine_appointment_patient = zip(appointments,patients)   
    return render(request,'doctor_dashboard.html',{"patientscount":patientscount,"appointmentscount":appointmentscount,"combine_appointment_patient":combine_appointment_patient,"doctor_profile_pic":doctor_profile_pic})


def doctor_view_patient(request):
    patients =  Patientmodel.objects.all().filter(status = True,assignedDoctorId = request.user.id)
    #profile pic
    doctor_profile_pic = Doctormodel.objects.get(user_id = request.user.id)
    return render(request,"doctor_view_patients.html",{"patients":patients,"doctor_profile_pic":doctor_profile_pic})

def doctor_view_him_appointments(request):
    doctor_profile_pic = Doctormodel.objects.get(user_id = request.user.id)
    appointments =  Appointmentmodel.objects.all().filter(status = True,doctorId = request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patient = Patientmodel.objects.all().filter(status = True,user_id__in = patientid)
    combine_appointments_and_patients = zip(appointments,patient)   
    return render(request,"doctor_view_him_appointments.html",{"combine_appointments_and_patients":combine_appointments_and_patients,"doctor_profile_pic":doctor_profile_pic}) 
       



##<=============  patients views ==============>

def patient_dashboard(request):
    patient_profile_pic = Patientmodel.objects.get(user_id = request.user.id)
    doctors = Doctormodel.objects.all()
    return render(request,'patient_dashboard.html',{"patient_profile_pic":"patient_profile_pic","doctors":doctors,"patient_profile_pic":patient_profile_pic})

def patient_request_for_appointment(request):
    PatientRequestedAppointmentform = PatientRequestForAppointment()
    patient_profile_pic = Patientmodel.objects.get(user_id = request.user.id)
    if request.method == "POST":
        PatientRequestedAppointmentform = PatientRequestForAppointment(request.POST)
        if PatientRequestedAppointmentform.is_valid():
            request.POST.get("doctorId")
            doctor=Doctormodel.objects.get(user_id=request.POST.get('doctorId'))
            patientform = PatientRequestedAppointmentform.save(commit = False)
            patientform.patientId = request.user.id
            patientform.doctorId= request.POST.get("doctorId")
            patientform.doctorName = User.objects.get(id = request.POST.get("doctorId")).first_name
            patientform.patientName = request.user.last_name
            patientform.status = False
            patientform.save()
        return HttpResponseRedirect("patient_dashboard")    
    
    return render(request,"patient_request_for_appointment.html",{"PatientRequestedAppointmentform":PatientRequestedAppointmentform,"patient_profile_pic":patient_profile_pic})

def status_of_appointments_of_patient(request):
    StatusOfAppointmentsOfPatient = Appointmentmodel.objects.all().filter(patientId = request.user.id)
    # For profile pic of patient
    patient_profile_pic = Patientmodel.objects.get(user_id = request.user.id)
    
    return render(request,"status_of_appointments_of_patient.html",{"StatusOfAppointmentsOfPatient":StatusOfAppointmentsOfPatient,"patient_profile_pic":patient_profile_pic})


