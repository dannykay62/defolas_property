from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.properties, name='properties'),
    path('properties/add/', views.add_property, name='add_property'),
    path('properties/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:pk>/delete/', views.delete_property, name='delete_property'),
    path('images/<int:pk>/delete/', views.delete_image, name='delete_image'),
    path('inquiries/', views.inquiries, name='inquiries'),
    path('inquiries/<int:pk>/', views.inquiry_detail, name='inquiry_detail'),
    path('locations/', views.locations, name='locations'),
    path('locations/<int:pk>/delete/', views.delete_location, name='delete_location'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('team/', views.team, name='team'),
]