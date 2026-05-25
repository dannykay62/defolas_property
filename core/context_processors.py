from django.conf import settings as django_settings


def site_context(request):
    return {
        'SITE_NAME': getattr(django_settings, 'SITE_NAME', "Defola's Properties"),
        'SITE_TAGLINE': getattr(django_settings, 'SITE_TAGLINE', 'Your Trusted Real Estate Partner in Nigeria'),
        'WHATSAPP_NUMBER': getattr(django_settings, 'WHATSAPP_NUMBER', '+2347061536383'),
        'PHONE_NUMBER': getattr(django_settings, 'PHONE_NUMBER', '+2347061536383'),
        'CONTACT_EMAIL': getattr(django_settings, 'CONTACT_EMAIL', 'info@defolasproperties.com'),
    }
