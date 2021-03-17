from django.shortcuts import render


# Create your views here.

def Home(request):

    return render(request,'site/index.html',{Home:'Home'})
def login(request):
    return render(request, 'Reg/register.html', {Home: 'Home'})