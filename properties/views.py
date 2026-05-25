from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from .models import Property, Location, Inquiry, SavedProperty, PropertyImage
from .forms import InquiryForm, PropertySearchForm


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/list.html'
    context_object_name = 'properties'
    paginate_by = 12

    def get_queryset(self):
        qs = Property.objects.prefetch_related('images').select_related('location')
        form = PropertySearchForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data.get('q')
            location = form.cleaned_data.get('location')
            property_type = form.cleaned_data.get('property_type')
            status = form.cleaned_data.get('status')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            bedrooms = form.cleaned_data.get('bedrooms')

            if q:
                qs = qs.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q) |
                    Q(address__icontains=q)
                )
            if location:
                qs = qs.filter(location=location)
            if property_type:
                qs = qs.filter(property_type=property_type)
            if status:
                qs = qs.filter(status=status)
            if min_price:
                qs = qs.filter(price__gte=min_price)
            if max_price:
                qs = qs.filter(price__lte=max_price)
            if bedrooms:
                qs = qs.filter(bedrooms__gte=bedrooms)

        sort = self.request.GET.get('sort', '-date_listed')
        valid_sorts = ['-date_listed', 'date_listed', 'price', '-price']
        if sort in valid_sorts:
            qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = PropertySearchForm(self.request.GET)
        ctx['locations'] = Location.objects.all()
        ctx['property_types'] = Property.TYPE_CHOICES
        ctx['total_count'] = self.get_queryset().count()
        ctx['current_sort'] = self.request.GET.get('sort', '-date_listed')
        ctx['page_title'] = 'All Properties'
        ctx['meta_description'] = "Browse all available properties for sale in Nigeria. Find land, apartments, duplexes and more."
        return ctx


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/detail.html'
    context_object_name = 'property'

    def get_object(self):
        return get_object_or_404(Property, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        prop = self.object
        ctx['inquiry_form'] = InquiryForm(initial={'property': prop.pk})
        ctx['similar'] = Property.objects.filter(
            property_type=prop.property_type,
            status='available'
        ).exclude(pk=prop.pk).prefetch_related('images')[:4]
        ctx['is_saved'] = False
        if self.request.user.is_authenticated:
            ctx['is_saved'] = SavedProperty.objects.filter(
                user=self.request.user, property=prop
            ).exists()
        ctx['page_title'] = prop.title
        ctx['meta_description'] = prop.meta_description
        ctx['og_image'] = prop.primary_image.image.url if prop.primary_image else ''
        return ctx


def property_inquiry(request, slug):
    prop = get_object_or_404(Property, slug=slug)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = prop
            inquiry.ip_address = get_client_ip(request)
            inquiry.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Inquiry sent successfully!'})
            messages.success(request, "Thank you! Your inquiry has been received. We'll contact you shortly.")
            return redirect('properties:detail', slug=slug)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('properties:detail', slug=slug)


def general_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.ip_address = get_client_ip(request)
            inquiry.save()
            messages.success(request, "Thank you for contacting us! We'll get back to you within 24 hours.")
            return redirect('core:contact')
    return redirect('core:contact')


@login_required
def toggle_save_property(request, slug):
    prop = get_object_or_404(Property, slug=slug)
    saved, created = SavedProperty.objects.get_or_create(user=request.user, property=prop)
    if not created:
        saved.delete()
        saved_status = False
        msg = 'Property removed from saved list.'
    else:
        saved_status = True
        msg = 'Property saved to your list!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved_status, 'message': msg})
    messages.success(request, msg)
    return redirect('properties:detail', slug=slug)


@login_required
def saved_properties(request):
    saved = SavedProperty.objects.filter(user=request.user).select_related('property').prefetch_related('property__images')
    return render(request, 'properties/saved.html', {
        'saved_properties': saved,
        'page_title': 'Saved Properties',
    })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
