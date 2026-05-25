from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='list'),
    path('saved/', views.saved_properties, name='saved'),
    path('inquiry/', views.general_inquiry, name='general_inquiry'),
    path('<slug:slug>/', views.PropertyDetailView.as_view(), name='detail'),
    path('<slug:slug>/inquiry/', views.property_inquiry, name='inquiry'),
    path('<slug:slug>/save/', views.toggle_save_property, name='save'),
]
