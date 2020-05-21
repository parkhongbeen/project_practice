from django.urls import path

from home import views

urlpatterns = [
    path('home/', views.Home, name='home')
]