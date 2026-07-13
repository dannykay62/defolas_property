from django.shortcuts import render, redirect
from django.contrib import messages
from properties.models import Property, Testimonial, Location
from properties.forms import InquiryForm, PropertySearchForm
from .models import SiteSettings, TeamMember
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")


def home(request):
    featured = Property.objects.filter(is_featured=True, status='available').prefetch_related('images')[:6]
    recent = Property.objects.filter(status='available').prefetch_related('images').order_by('-date_listed')[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    locations = Location.objects.all()[:8]
    stats = {
        'available': Property.objects.filter(status='available').count(),
        'sold': Property.objects.filter(status='sold').count(),
        'locations': Location.objects.count(),
    }
    return render(request, 'core/home.html', {
        'featured_properties': featured,
        'recent_properties': recent,
        'testimonials': testimonials,
        'locations': locations,
        'stats': stats,
        'search_form': PropertySearchForm(),
        'page_title': "Defola's Properties - Premium Real Estate in Nigeria",
        'meta_description': "Find your dream property in Nigeria with Defola's Properties. Premium land, apartments, duplexes and commercial spaces in Lagos and beyond.",
    })


def about(request):
    team = TeamMember.objects.filter(is_active=True)
    return render(request, 'core/about.html', {
        'team_members': team,
        'page_title': "About Us - Defola's Properties",
        'meta_description': "Learn about Defola's Properties - Nigeria's trusted real estate company with years of experience helping clients find their perfect properties.",
    })


def contact(request):
    form = InquiryForm()
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                inquiry.ip_address = x_forwarded_for.split(',')[0]
            else:
                inquiry.ip_address = request.META.get('REMOTE_ADDR')
            inquiry.save()
            messages.success(request, "Thank you for reaching out! We'll get back to you within 24 hours.")
            return redirect('core:contact')
    return render(request, 'core/contact.html', {
        'form': form,
        'page_title': "Contact Us - Defola's Properties",
        'meta_description': "Contact Defola's Properties for all your real estate needs. Call, WhatsApp or email us today.",
    })
