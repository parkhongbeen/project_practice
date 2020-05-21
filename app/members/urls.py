from django.urls import path

from members import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('naver-login/', views.naver_login, name='naver-login'),

]
