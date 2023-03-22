from django.urls import path
from apps.testapp import views

urlpatterns = [
    path('', views.log, name='log'),
]
