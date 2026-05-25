from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter
def naira(value):
    try:
        return f"₦{float(value):,.0f}"
    except (ValueError, TypeError):
        return value


@register.filter
def star_rating(value):
    try:
        value = int(value)
        stars = '★' * value + '☆' * (5 - value)
        return mark_safe(f'<span class="text-yellow-400">{stars}</span>')
    except:
        return ''


@register.simple_tag
def property_badge(status):
    badges = {
        'available': 'bg-emerald-500 text-white',
        'pending': 'bg-amber-500 text-white',
        'sold': 'bg-red-500 text-white',
    }
    label = {'available': 'Available', 'pending': 'Pending', 'sold': 'Sold'}.get(status, status)
    css = badges.get(status, 'bg-gray-500 text-white')
    return mark_safe(f'<span class="px-2 py-1 text-xs font-bold rounded-full {css}">{label}</span>')


@register.filter
def youtube_embed(url):
    """Convert YouTube URL to embed URL"""
    if not url:
        return ''
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    return url
