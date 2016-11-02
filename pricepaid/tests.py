from random import randint

from django.test import TestCase

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import PricePaidEntry, Town
from .serializers import PricePaidEntrySerializer


class PricePaidAPITestCase(APITestCase):
    fixtures = ['test_data.yaml']

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@nowhere.org', 'adminsecret')
        self.client.login(username='admin', password='adminsecret')

    def test_can_list(self):
        response = self.client.get(reverse('pricepaidentry-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_detail(self):
        random_index = randint(0, PricePaidEntry.objects.count() - 1)
        oid = PricePaidEntry.objects.all()[random_index].pk
        response = self.client.get(reverse('pricepaidentry-detail', args=[oid]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_stats(self):
        response = self.client.get(reverse('pricepaidstats-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_search_stats(self):
        random_index = randint(0, Town.objects.count() - 1)
        oid = Town.objects.all()[random_index].pk
        response = self.client.get(reverse('pricepaidstats-list'), town=oid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for rec in response.data['results']:
            self.assertTrue(rec['min_price'] <= rec['avg_price'] <= rec['max_price'], 'price min<avg<max')


class PricePaidUITestCase(TestCase):
    fixtures = ['test_data.yaml']

    def test_can_open_page(self):
        response = self.client.get(reverse('pricepaid.views.index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
