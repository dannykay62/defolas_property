from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os


class Location(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Lagos')
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.state}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state}"


class Property(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ]
    TYPE_CHOICES = [
        ('land', 'Land'),
        ('apartment', 'Apartment'),
        ('duplex', 'Duplex'),
        ('bungalow', 'Bungalow'),
        ('commercial', 'Commercial'),
        ('office', 'Office Space'),
        ('warehouse', 'Warehouse'),
        ('estate', 'Estate'),
        ('terrace', 'Terrace'),
        ('mansion', 'Mansion'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='properties')
    address = models.CharField(max_length=300)
    property_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    bedrooms = models.PositiveIntegerField(default=0, help_text="0 for land/commercial")
    bathrooms = models.PositiveIntegerField(default=0)
    toilets = models.PositiveIntegerField(default=0)
    size_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Size in sqm")
    is_featured = models.BooleanField(default=False)
    is_negotiable = models.BooleanField(default=False)

    # SEO
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    # Video
    video_url = models.URLField(blank=True, help_text="YouTube or any video URL")
    virtual_tour_url = models.URLField(blank=True)

    date_listed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    listed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Amenities
    has_parking = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_generator = models.BooleanField(default=False)
    has_water_supply = models.BooleanField(default=False)
    has_cctv = models.BooleanField(default=False)
    is_serviced = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-date_listed']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        if not self.meta_description:
            self.meta_description = f"{self.title} - {self.property_type.title()} for sale in {self.address}. Price: ₦{self.price:,.0f}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})

    def get_whatsapp_url(self):
        from django.conf import settings
        message = f"Hello, I'm interested in this property: {self.title} - {self.get_absolute_url()}"
        import urllib.parse
        return f"https://wa.me/{settings.WHATSAPP_NUMBER.replace('+', '')}?text={urllib.parse.quote(message)}"

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def formatted_price(self):
        return f"₦{self.price:,.0f}"

    @property
    def amenities_list(self):
        amenities = []
        if self.has_parking: amenities.append(('Parking', 'car'))
        if self.has_security: amenities.append(('24/7 Security', 'shield'))
        if self.has_pool: amenities.append(('Swimming Pool', 'droplets'))
        if self.has_gym: amenities.append(('Gym', 'dumbbell'))
        if self.has_generator: amenities.append(('Generator', 'zap'))
        if self.has_water_supply: amenities.append(('Water Supply', 'droplet'))
        if self.has_cctv: amenities.append(('CCTV', 'camera'))
        if self.is_serviced: amenities.append(('Serviced', 'star'))
        return amenities

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        # Ensure only one primary image per property
        if self.is_primary:
            PropertyImage.objects.filter(property=self.property, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='properties/videos/%Y/%m/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Video for {self.property.title}"


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('inspection', 'Schedule Inspection'),
        ('offer', 'Make an Offer'),
        ('info', 'Request More Info'),
    ]

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='general')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    preferred_date = models.DateField(null=True, blank=True, help_text="Preferred inspection date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.property.title if self.property else 'General'} ({self.created_at.strftime('%d/%m/%Y')})"


class SavedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'property']

    def __str__(self):
        return f"{self.user.username} saved {self.property.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Client')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"
