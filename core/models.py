from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Defola's Properties")
    tagline = models.CharField(max_length=200, default="Your Trusted Real Estate Partner")
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    about_text = models.TextField(blank=True)
    about_image = models.ImageField(upload_to='site/', blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=10)
    properties_sold = models.PositiveIntegerField(default=500)
    happy_clients = models.PositiveIntegerField(default=450)
    team_members = models.PositiveIntegerField(default=20)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
