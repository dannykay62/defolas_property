from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
from properties.models import Property, Location, Inquiry, Testimonial
from core.models import TeamMember


def dashboard_context(request):
    return {
        'total_properties': Property.objects.count(),
        'new_inquiries_count': Inquiry.objects.filter(status='new').count(),
    }


@staff_member_required(login_url='/accounts/login/')
def home(request):
    stats = {
        'total': Property.objects.count(),
        'available': Property.objects.filter(status='available').count(),
        'pending': Property.objects.filter(status='pending').count(),
        'sold': Property.objects.filter(status='sold').count(),
        'new_inquiries': Inquiry.objects.filter(status='new').count(),
    }
    type_breakdown = Property.objects.values('property_type').annotate(count=Count('id')).order_by('-count')
    recent_properties = Property.objects.prefetch_related('images').order_by('-date_listed')[:6]
    recent_inquiries = Inquiry.objects.filter(status='new').order_by('-created_at')[:5]
    return render(request, 'dashboard/home.html', {
        **dashboard_context(request),
        'stats': stats,
        'type_breakdown': type_breakdown,
        'recent_properties': recent_properties,
        'recent_inquiries': recent_inquiries,
    })


@staff_member_required(login_url='/accounts/login/')
def properties(request):
    qs = Property.objects.prefetch_related('images').select_related('location').order_by('-date_listed')
    status = request.GET.get('status')
    ptype = request.GET.get('type')
    q = request.GET.get('q')
    if status:
        qs = qs.filter(status=status)
    if ptype:
        qs = qs.filter(property_type=ptype)
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'dashboard/properties.html', {
        **dashboard_context(request),
        'properties': qs,
        'total': qs.count(),
        'status_filter': status,
        'type_filter': ptype,
        'q': q or '',
        'property_types': Property.TYPE_CHOICES,
    })


@staff_member_required(login_url='/accounts/login/')
def add_property(request):
    from properties.forms import PropertyForm
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.listed_by = request.user
            prop.save()
            # Handle multiple images
            images = request.FILES.getlist('images')
            from properties.models import PropertyImage
            for i, img in enumerate(images):
                PropertyImage.objects.create(
                    property=prop, image=img, is_primary=(i == 0), order=i
                )
            messages.success(request, f'Property "{prop.title}" added successfully!')
            return redirect('dashboard:properties')
    else:
        form = PropertyForm()
    return render(request, 'dashboard/property_form.html', {
        **dashboard_context(request),
        'form': form,
        'title': 'Add Property',
        'is_edit': False,
    })


@staff_member_required(login_url='/accounts/login/')
def edit_property(request, pk):
    from properties.forms import PropertyForm
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            from properties.models import PropertyImage
            for i, img in enumerate(images):
                PropertyImage.objects.create(
                    property=prop, image=img, order=prop.images.count() + i
                )
            messages.success(request, f'Property "{prop.title}" updated successfully!')
            return redirect('dashboard:properties')
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'dashboard/property_form.html', {
        **dashboard_context(request),
        'form': form,
        'property': prop,
        'existing_images': prop.images.all(),
        'title': f'Edit: {prop.title}',
        'is_edit': True,
    })


@staff_member_required(login_url='/accounts/login/')
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        title = prop.title
        prop.delete()
        messages.success(request, f'"{title}" deleted successfully.')
    return redirect('dashboard:properties')


@staff_member_required(login_url='/accounts/login/')
def delete_image(request, pk):
    from properties.models import PropertyImage
    from django.http import JsonResponse
    img = get_object_or_404(PropertyImage, pk=pk)
    img.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('dashboard:edit_property', pk=img.property.pk)


@staff_member_required(login_url='/accounts/login/')
def inquiries(request):
    qs = Inquiry.objects.select_related('property').order_by('-created_at')
    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)
    return render(request, 'dashboard/inquiries.html', {
        **dashboard_context(request),
        'inquiries': qs,
        'status_filter': status,
    })


@staff_member_required(login_url='/accounts/login/')
def inquiry_detail(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if inquiry.status == 'new':
        inquiry.status = 'in_progress'
        inquiry.save()
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['new', 'in_progress', 'resolved']:
            inquiry.status = new_status
            inquiry.save()
            messages.success(request, 'Inquiry status updated.')
        return redirect('dashboard:inquiry_detail', pk=pk)
    return render(request, 'dashboard/inquiry_detail.html', {
        **dashboard_context(request),
        'inquiry': inquiry,
    })


@staff_member_required(login_url='/accounts/login/')
def locations(request):
    locs = Location.objects.annotate(prop_count=Count('properties')).order_by('name')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        state = request.POST.get('state', '').strip()
        if name and state:
            Location.objects.create(name=name, state=state)
            messages.success(request, f'Location "{name}" added.')
        return redirect('dashboard:locations')
    return render(request, 'dashboard/locations.html', {
        **dashboard_context(request),
        'locations': locs,
    })


@staff_member_required(login_url='/accounts/login/')
def delete_location(request, pk):
    loc = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        loc.delete()
        messages.success(request, 'Location deleted.')
    return redirect('dashboard:locations')


@staff_member_required(login_url='/accounts/login/')
def testimonials(request):
    from properties.models import Testimonial
    items = Testimonial.objects.order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'delete' and pk:
            Testimonial.objects.filter(pk=pk).delete()
            messages.success(request, 'Testimonial deleted.')
        elif action == 'toggle' and pk:
            t = get_object_or_404(Testimonial, pk=pk)
            t.is_active = not t.is_active
            t.save()
        return redirect('dashboard:testimonials')
    return render(request, 'dashboard/testimonials.html', {
        **dashboard_context(request),
        'testimonials': items,
    })


@staff_member_required(login_url='/accounts/login/')
def team(request):
    members = TeamMember.objects.order_by('order')
    if request.method == 'POST':
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        if action == 'delete' and pk:
            TeamMember.objects.filter(pk=pk).delete()
            messages.success(request, 'Team member deleted.')
        elif action == 'toggle' and pk:
            m = get_object_or_404(TeamMember, pk=pk)
            m.is_active = not m.is_active
            m.save()
        return redirect('dashboard:team')
    return render(request, 'dashboard/team.html', {
        **dashboard_context(request),
        'members': members,
    })