from django.urls import path

from members import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
]