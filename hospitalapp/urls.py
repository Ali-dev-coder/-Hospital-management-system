from unicodedata import name
from django.urls import path
from .views import (admin_dashboardviews,
                    admin_view_approved_doctor_records,
                    admin_add_doctors,
                    admin_update_doctor_record,
                    admin_view_pending_doctor_names,
                    admin_add_patients,
                    admin_view_admitted_patients_records,
                    admin_view_pending_patients_names,
                    admin_view_all_appointments,
                    admin_add_appointments,
                    doctor_dashboard,
                    doctor_view_patient,
                    home,
                    patient_dashboard,
                    afterlogin_redirect,
                    admin_sign_up,
                    doctor_sign_up,
                    patient_sign_up,
                    patient_request_for_appointment,
                    status_of_appointments_of_patient,
                    admin_approved_pending_patient,
                    admin_delete_pending_patient,
                    admin_update_patients,
                    admin_delete_approved_patient,
                    admin_approved_pending_doctor,
                    admin_delete_pending_doctor,
                    admin_delete_doctor_from_hospital,
                    admin_approved_the_pending_appointments,
                    admin_delete_pending_appointments,
                    admin_view_pending_appointment,
                    admin_delete_approved_appointments,
                    doctor_view_him_appointments
                    )


# from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    
    ## <===== HOME PAGE ====>
    path("",home,name = "home"),
    ##<===== Admin Urls ====>
    path("admin_sign_up",admin_sign_up,name = "admin_sign_up"),
    # path("adminlogin",LoginView.as_view(template_name = "adminlogin.html")),
    path("admin_dashboard",admin_dashboardviews, name='admin_dashboard'),
    path("admin-view-approved-doctor-records",admin_view_approved_doctor_records, name='admin-view-approved-doctor-records'),
    path("admin_add_doctors",admin_add_doctors,name = "admin_add_doctors"),
    path("admin_update_doctor_record/<int:pk>",admin_update_doctor_record,name="admin_update_doctor_record"),
    path("admin_view_pending_doctor_names",admin_view_pending_doctor_names,name="admin_view_pending_doctor_names"),
    path("admin_add_patients",admin_add_patients,name = "admin_add_patients"),
    path("admin_view_admitted_patients_records",admin_view_admitted_patients_records,name = "admin_view_admitted_patients_records"),
    path("admin_view_pending_patients_names",admin_view_pending_patients_names,name = "admin_view_pending_patients_names"),
    path("admin_view_all_appointments",admin_view_all_appointments,name = "admin_view_all_appointments"),
    path("admin_add_appointments",admin_add_appointments,name = "admin_add_appointments"),
    path("admin_approved_pending_patient/<int:pk>",admin_approved_pending_patient,name = "admin_approved_pending_patient"),
    path("admin_delete_pending_patient/<int:pk>",admin_delete_pending_patient,name = "admin_delete_pending_patient"),
    path("admin_update_patients/<int:pk>",admin_update_patients,name = "admin_update_patients"),
    path("admin_delete_approved_patient/<int:pk>",admin_delete_approved_patient,name = "admin_delete_approved_patient"),
    path("admin_approved_pending_doctor/<int:pk>",admin_approved_pending_doctor,name = "admin_approved_pending_doctor"),
    path("admin_delete_pending_doctor/<int:pk>",admin_delete_pending_doctor,name = "admin_delete_pending_doctor"),
    path("admin_delete_doctor_from_hospital/<int:pk>",admin_delete_doctor_from_hospital,name = "admin_delete_doctor_from_hospital"),
    path("admin_view_pending_appointment",admin_view_pending_appointment,name = "admin_view_pending_appointment"),
    path("admin_approved_the_pending_appointments/<int:pk>",admin_approved_the_pending_appointments,name = "admin_approved_the_pending_appointments"),
    path("admin_delete_pending_appointments/<int:pk>",admin_delete_pending_appointments,name = "admin_delete_pending_appointments"),
    path("admin_delete_approved_appointments/<int:pk>",admin_delete_approved_appointments,name = "admin_delete_approved_appointments"),
    path("doctor_view_him_appointments",doctor_view_him_appointments,name = "doctor_view_him_appointments"),
    
    
    ##<====  doctor urls ====>
    
    path("doctor_sign_up",doctor_sign_up,name = "doctor_sign_up"),
    # path("doctorlogin",LoginView.as_view(template_name = "doctorlogin.html")),
    path("doctor_dashboard",doctor_dashboard,name="doctor_dashboard"),
    path("doctor_view_patient",doctor_view_patient,name = "doctor_view_patient"),
    
    path("logout",LogoutView.as_view(template_name = "index.html"),name = "logout"),
    
    ##<======== patients urls===============>
    # path("patientlogin",LoginView.as_view(template_name = "patientlogin.html")),
    path("patient_sign_up",patient_sign_up,name = "patient_sign_up"),
    path("patient_dashboard",patient_dashboard,name="patient_dashboard"),
    path("patient_request_for_appointment",patient_request_for_appointment,name = "patient_request_for_appointment"),
    path("status_of_appointments_of_patient",status_of_appointments_of_patient,name = "status_of_appointments_of_patient"),
    
    
    
  
    
    
    
    ##<========= afterlogin redirect========>
    path("afterlogin_redirect",afterlogin_redirect,name = "afterlogin_redirect")
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
