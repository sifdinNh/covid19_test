from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisteruserForm, RegisterCitoyen, RDV_Register
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from .models import *

from .forms import  *
# Create your views here.
def register(request):
    user = request.user
    if user.is_authenticated:
        return redirect('Home')
    userForm = RegisteruserForm()
    patientForm = RegisterCitoyen()
    if request.method == 'POST':
        userForm = RegisteruserForm(request.POST)
        patientForm = RegisterCitoyen(request.POST)

        print(patientForm.errors)

        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            print("here")
            user.set_password(user.password)
            user.save()
            citoyen = patientForm.save(commit=False)
            citoyen.user = user
            citoyen = citoyen.save()
            my_patient_group = Group.objects.get_or_create(name='CITOYEN')
            my_patient_group[0].user_set.add(user)
            login(request,user)
            return redirect('Home')


    mydict = {'userForm': userForm, 'patientForm': patientForm}
    return render(request, 'Reg/register.html', context=mydict)
def Rdv(request):
    if request.method == "POST":
        form=RDV_Register(request.POST)
        form2 = UpdateUser(request.POST, request.FILES, instance=request.user)
        print("form.errors")
        if form.is_valid() and form2.is_valid():
            Rdv = form.save(commit=False)
            Rdv.citoyen = request.user.citoyen
            Rdv.center_id = form.cleaned_data['choice_field']
            request.user.citoyen.cov_19 = form.cleaned_data['is_cov19']
            request.user.citoyen.RAMID = form.cleaned_data['ramid']
            print(Rdv.center_id)
            request.user.citoyen.is_RDV = True
            request.user.citoyen.save()
            form.save()
            form2.save()
            print(form.errors)


    else:
        form=RDV_Register()
        form2=UpdateUser()
    return render(request, 'Reg/RDV.html', context={'form':form,'formImage':form2})
def Rdv_management(request):
    C_id=request.user.administrateur.centre.pk
    Rdv=RDV.objects.filter(is_confirmed=False,is_rejected=False, center_id=C_id)
    return render(request, 'administrateur/test.html', context={'Rdv':Rdv})
def profile(request, id):
    citoyen = Citoyen.objects.get(pk=id)
    Rdv = RDV.objects.get(citoyen=citoyen)
    centre = Centre.objects.get(pk=Rdv.center_id)
    return render(request, 'administrateur/profile.html', context={'Rdv': Rdv,'citoyen':citoyen,'centre':centre})

def delete(request, id):
    citoyen=Citoyen.objects.get(pk=id)
    Rdv=RDV.objects.get(citoyen=citoyen)
    Rdv.is_rejected=True
    Rdv.save();
    return redirect('Rdv_management')
def accept(request, id):
    citoyen=Citoyen.objects.get(pk=id)
    Rdv=RDV.objects.get(citoyen=citoyen)
    Rdv.is_confirmed=True
    Rdv.save();
    return redirect('Rdv_management')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")