from django.shortcuts import render


# Create your views here.


class Home(request):
    context = {

    }
    return render(request, 'home/home.html' context)
