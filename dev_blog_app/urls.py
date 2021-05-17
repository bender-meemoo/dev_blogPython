from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path('loginuser', views.loginuser),
    path('createuser', views.createuser),
    path('logout', views.logout),
    path('blog', views.blog),
    path('addentry', views.addentry),
    path('asset', views.asset)
]