from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:short_code>/', views.redirect_to_original, name='redirect'),
]