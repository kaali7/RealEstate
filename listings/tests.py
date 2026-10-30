from django.test import TestCase

from realtors.models import Realtor
from .models import Listing


class ListingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        realtor = Realtor.objects.create(
            name='Test Realtor',
            photo='photos/realtor.jpg',
            phone='1234567890',
            email='test@example.com',
        )
        cls.listing = Listing.objects.create(
            realtor=realtor,
            title='Test Luxury Home',
            address='1 Test Street',
            city='Test City',
            state='Maharashtra',
            zipcode='12345',
            description='Includes a private swimming pool and modern garage amenities.',
            price=10000000,
            bedrooms=3,
            bathrooms=2,
            garage=2,
            sqft=1500,
            lot_size=2000,
            photo_main='photos/test.jpg',
        )

    def test_listings_page_loads(self):
        response = self.client.get('/listings/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.title)

    def test_listing_detail_loads(self):
        response = self.client.get('/listings/%s' % self.listing.pk)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.title)

    def test_search_filters_by_city(self):
        response = self.client.get('/listings/search', {'city': 'Test City'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.title)

    def test_search_filters_by_keyword(self):
        # Search by word in description
        response = self.client.get('/listings/search', {'keywords': 'swimming pool'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.title)

        # Search by word in title
        response2 = self.client.get('/listings/search', {'keywords': 'Luxury'})
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, self.listing.title)

    def test_search_filters_by_price(self):
        response = self.client.get('/listings/search', {'price': '10000000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.title)

    def test_legacy_nested_listings_url_redirects(self):
        response = self.client.get('/listings/listings.html')

        self.assertRedirects(response, '/listings/')
