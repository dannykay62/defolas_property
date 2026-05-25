from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Property, PropertyImage, PropertyVideo, Location, Inquiry, SavedProperty, Testimonial


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ['image', 'caption', 'is_primary', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:100px;height:70px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1
    fields = ['video', 'video_url', 'title']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'property_type', 'location', 'formatted_price', 'status_badge', 'is_featured', 'date_listed']
    list_display_links = ['thumbnail', 'title']
    list_filter = ['status', 'property_type', 'location', 'is_featured', 'date_listed']
    search_fields = ['title', 'address', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured']
    readonly_fields = ['date_listed', 'date_updated', 'listed_by']
    inlines = [PropertyImageInline, PropertyVideoInline]
    list_per_page = 20
    save_on_top = True
    actions = ['mark_available', 'mark_sold', 'mark_pending', 'mark_featured', 'unmark_featured']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'property_type', 'status', 'is_featured', 'is_negotiable')
        }),
        ('Location & Pricing', {
            'fields': ('location', 'address', 'price')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'toilets', 'size_sqm')
        }),
        ('Amenities', {
            'fields': ('has_parking', 'has_security', 'has_pool', 'has_gym', 'has_generator', 'has_water_supply', 'has_cctv', 'is_serviced'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('video_url', 'virtual_tour_url'),
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('date_listed', 'date_updated', 'listed_by'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        img = obj.primary_image
        if img:
            return format_html('<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:6px;" />', img.image.url)
        return format_html('<div style="width:60px;height:45px;background:#e2e8f0;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#64748b;">No img</div>')
    thumbnail.short_description = ''

    def formatted_price(self, obj):
        price = obj.price or 0
        formatted_price = f"₦{price:,.0f}"
        return format_html(
            '<strong style="color:#0d9488;">{}</strong>',
            formatted_price
        )

    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'

    def status_badge(self, obj):
        colors = {
            'available': '#10b981',
            'pending': '#f59e0b',
            'sold': '#ef4444',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='Mark selected as Available')
    def mark_available(self, request, queryset):
        queryset.update(status='available')
        self.message_user(request, f"{queryset.count()} properties marked as Available.")

    @admin.action(description='Mark selected as Sold')
    def mark_sold(self, request, queryset):
        queryset.update(status='sold')
        self.message_user(request, f"{queryset.count()} properties marked as Sold.")

    @admin.action(description='Mark selected as Pending')
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, f"{queryset.count()} properties marked as Pending.")

    @admin.action(description='Mark selected as Featured')
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description='Remove from Featured')
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'property_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'state']

    def property_count(self, obj):
        return obj.properties.count()
    property_count.short_description = 'Properties'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'property_link', 'inquiry_type', 'status_badge', 'created_at']
    list_filter = ['status', 'inquiry_type', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['name', 'email', 'phone', 'message', 'property', 'created_at', 'ip_address', 'preferred_date', 'inquiry_type']
    list_per_page = 25
    actions = ['mark_in_progress', 'mark_resolved']

    def property_link(self, obj):
        if obj.property:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.property.get_absolute_url(), obj.property.title[:40])
        return 'General Inquiry'
    property_link.short_description = 'Property'

    def status_badge(self, obj):
        colors = {'new': '#3b82f6', 'in_progress': '#f59e0b', 'resolved': '#10b981'}
        color = colors.get(obj.status, '#6b7280')
        return format_html('<span style="background:{};color:white;padding:3px 8px;border-radius:10px;font-size:11px;">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'

    @admin.action(description='Mark as In Progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(description='Mark as Resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'is_active', 'created_at']
    list_editable = ['is_active']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'property', 'is_primary', 'order']
    list_editable = ['is_primary', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px;height:55px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


# Customize Admin Site
admin.site.site_header = "Defola's Properties Admin"
admin.site.site_title = "Defola's Properties"
admin.site.index_title = "Property Management Dashboard"
