from django.urls import path
from . import views
from core.views import health_check


app_name = 'core'

urlpatterns = [
    path("healthz", health_check),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
