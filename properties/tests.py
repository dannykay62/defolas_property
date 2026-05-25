from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Property, Location, Inquiry, PropertyImage, SavedProperty


class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='Lekki', state='Lagos')

    def test_location_str(self):
        self.assertEqual(str(self.location), 'Lekki, Lagos')

    def test_location_slug_auto_generated(self):
        self.assertIsNotNone(self.location.slug)
        self.assertIn('lekki', self.location.slug)


class PropertyModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='Victoria Island', state='Lagos')
        self.property = Property.objects.create(
            title='Luxury 4-Bedroom Duplex in VI',
            description='A beautiful duplex in Victoria Island.',
            price=250000000,
            location=self.location,
            address='Victoria Island, Lagos',
            property_type='duplex',
            status='available',
            bedrooms=4,
            bathrooms=4,
        )

    def test_property_str(self):
        self.assertEqual(str(self.property), 'Luxury 4-Bedroom Duplex in VI')

    def test_slug_auto_generated(self):
        self.assertIsNotNone(self.property.slug)
        self.assertIn('luxury', self.property.slug)

    def test_slug_is_unique(self):
        prop2 = Property.objects.create(
            title='Luxury 4-Bedroom Duplex in VI',
            description='Another duplex.',
            price=200000000,
            location=self.location,
            address='VI, Lagos',
            property_type='duplex',
            status='available',
        )
        self.assertNotEqual(self.property.slug, prop2.slug)

    def test_formatted_price(self):
        self.assertIn('₦', self.property.formatted_price)
        self.assertIn('250,000,000', self.property.formatted_price)

    def test_get_absolute_url(self):
        url = self.property.get_absolute_url()
        self.assertIn(self.property.slug, url)

    def test_meta_description_auto_generated(self):
        self.assertIsNotNone(self.property.meta_description)
        self.assertGreater(len(self.property.meta_description), 0)

    def test_primary_image_returns_none_when_no_images(self):
        self.assertIsNone(self.property.primary_image)


class PropertyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(name='Lekki', state='Lagos')
        self.property = Property.objects.create(
            title='Test Property in Lekki',
            description='A test property.',
            price=50000000,
            location=self.location,
            address='Lekki, Lagos',
            property_type='land',
            status='available',
        )

    def test_property_list_view(self):
        response = self.client.get(reverse('properties:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property in Lekki')

    def test_property_detail_view(self):
        response = self.client.get(reverse('properties:detail', kwargs={'slug': self.property.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property in Lekki')

    def test_property_detail_404_for_bad_slug(self):
        response = self.client.get(reverse('properties:detail', kwargs={'slug': 'nonexistent-slug'}))
        self.assertEqual(response.status_code, 404)

    def test_property_list_filter_by_type(self):
        Property.objects.create(
            title='Apartment in Lekki', description='An apartment.', price=80000000,
            location=self.location, address='Lekki, Lagos', property_type='apartment', status='available'
        )
        response = self.client.get(reverse('properties:list') + '?property_type=land')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property in Lekki')
        self.assertNotContains(response, 'Apartment in Lekki')

    def test_property_list_search(self):
        response = self.client.get(reverse('properties:list') + '?q=Test+Property')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property in Lekki')

    def test_property_list_pagination(self):
        for i in range(15):
            Property.objects.create(
                title=f'Property {i}', description='Test', price=10000000,
                location=self.location, address='Lagos', property_type='land', status='available'
            )
        response = self.client.get(reverse('properties:list'))
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)


class InquiryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(name='Ajah', state='Lagos')
        self.property = Property.objects.create(
            title='Land in Ajah', description='Nice land.', price=15000000,
            location=self.location, address='Ajah, Lagos', property_type='land', status='available'
        )

    def test_inquiry_submission(self):
        response = self.client.post(
            reverse('properties:inquiry', kwargs={'slug': self.property.slug}),
            {
                'inquiry_type': 'general',
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+2348012345678',
                'message': 'I am interested in this property.',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Inquiry.objects.count(), 1)
        inquiry = Inquiry.objects.first()
        self.assertEqual(inquiry.name, 'John Doe')
        self.assertEqual(inquiry.property, self.property)

    def test_inquiry_linked_to_property(self):
        self.client.post(
            reverse('properties:inquiry', kwargs={'slug': self.property.slug}),
            {
                'inquiry_type': 'inspection',
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone': '+2348087654321',
                'message': 'Please schedule an inspection.',
            }
        )
        inquiry = Inquiry.objects.first()
        self.assertEqual(inquiry.property.pk, self.property.pk)


class SavedPropertyTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.location = Location.objects.create(name='Ikoyi', state='Lagos')
        self.property = Property.objects.create(
            title='Apartment in Ikoyi', description='Nice apartment.', price=100000000,
            location=self.location, address='Ikoyi, Lagos', property_type='apartment', status='available'
        )

    def test_save_property_requires_login(self):
        response = self.client.post(reverse('properties:save', kwargs={'slug': self.property.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_user_can_save_property(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('properties:save', kwargs={'slug': self.property.slug}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SavedProperty.objects.count(), 1)

    def test_authenticated_user_can_unsave_property(self):
        self.client.login(username='testuser', password='testpass123')
        SavedProperty.objects.create(user=self.user, property=self.property)
        response = self.client.post(
            reverse('properties:save', kwargs={'slug': self.property.slug}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SavedProperty.objects.count(), 0)
