# rental/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Rental
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class RentalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student1', password='pass')
        self.book = Book.objects.create(title='Test Book', openlibrary_key='TEST123', number_of_pages=100)

    def test_rental_creation(self):
        rental = Rental.objects.create(user=self.user, book=self.book)
        self.assertEqual(rental.fees, 0)

    def test_fee_calculation_no_fee(self):
        rental = Rental.objects.create(user=self.user, book=self.book)
        rental.calculate_fees()
        self.assertEqual(rental.fees, 0)

    def test_fee_calculation_with_fee(self):
        rental = Rental.objects.create(user=self.user, book=self.book)
        rental.rental_date = timezone.now() - timedelta(days=31)
        rental.save()
        rental.calculate_fees()
        self.assertEqual(rental.fees, 1)

    def test_start_rental_view(self):
        self.client.login(username='student1', password='pass')
        response = self.client.post(reverse('rental:start_rental'), {'user': self.user.id, 'book_title': 'Python'})
        self.assertEqual(response.status_code, 302)  # Seharusnya redirect setelah berhasil

    def test_extend_rental_view(self):
        rental = Rental.objects.create(user=self.user, book=self.book)
        self.client.login(username='student1', password='pass')
        response = self.client.post(reverse('rental:extend_rental'), {'rental': rental.id})
        self.assertEqual(response.status_code, 302)  # Seharusnya redirect setelah berhasil
