from django.contrib import admin
from .models import SiteSettings, TeamMember


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {'fields': ('site_name', 'tagline', 'phone', 'whatsapp', 'email', 'address')}),
        ('Social Media', {'fields': ('facebook', 'instagram', 'twitter', 'youtube')}),
        ('About Page', {'fields': ('about_text', 'about_image')}),
        ('Stats', {'fields': ('years_experience', 'properties_sold', 'happy_clients', 'team_members')}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active', 'order']
    list_editable = ['is_active', 'order']
