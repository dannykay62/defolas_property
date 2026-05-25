from django import forms
from .models import Inquiry, Location, Property


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['inquiry_type', 'name', 'email', 'phone', 'message', 'preferred_date']
        widgets = {
            'inquiry_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent bg-white',
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'your@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': '+234 800 0000 000',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Tell us about your interest in this property...',
                'rows': 4,
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'type': 'date',
            }),
        }


class PropertySearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search properties, locations...',
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-teal-500',
    }))
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        empty_label="All Locations",
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-gray-200'})
    )
    property_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Property.TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-gray-200'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Property.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-gray-200'})
    )
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Min Price (₦)',
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200',
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Max Price (₦)',
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200',
    }))
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Min Bedrooms',
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200',
        'min': 0,
    }))



from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['slug', 'date_listed', 'date_updated', 'listed_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500', 'placeholder': 'Property title'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500', 'placeholder': '0'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'location': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'property_type': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'status': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'toilets': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'size_sqm': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'video_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500', 'placeholder': 'https://youtube.com/...'}),
            'virtual_tour_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500'}),
        }