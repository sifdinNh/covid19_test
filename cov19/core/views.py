from django.shortcuts import render
from accounts.models import RDV


# Create your views here.

def Home(request):
    Rdv=RDV.objects.all()
    print(Rdv)
    return render(request,'site/index.html',{Home:'Home',Rdv:'Rdv'})
def login(request):
    return render(request, 'Reg/register.html', {Home: 'Home'})