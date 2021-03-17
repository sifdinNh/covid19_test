from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisteruserForm, RegisterCitoyen, RDV_Register
from django.contrib.auth.models import Group

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
            form2.save()
            print("image")
           ## Rdv.citoyen.cov_19 = Rdv.is_cov19
           ## Rdv.center_id = Rdv.choice_field
           ## Rdv.save()

    else:
        form=RDV_Register()
        form2=UpdateUser()
    return render(request, 'Reg/RDV.html', context={'form':form,'formImage':form2})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")