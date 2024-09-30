# rentals/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class Book(models.Model):
    """
    Model representing a book retrieved from OpenLibrary.
    """
    title = models.CharField(max_length=255)
    openlibrary_key = models.CharField(max_length=100, unique=True)
    number_of_pages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Rental(models.Model):
    """
    Model representing a rental transaction between a user and a book.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    rental_date = models.DateTimeField(default=timezone.now)
    extended = models.BooleanField(default=False)
    fees = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    def calculate_fees(self):
        """
        Calculates the rental fees based on the number of days rented beyond the free period.
        """
        today = timezone.now().date()
        rental_date = self.rental_date.date()  # Ubah ke date
        rental_period = (today - rental_date).days
        if rental_period > 30:
            months_overdue = ((rental_period - 30) // 30) + 1
            fee_per_month = Decimal(self.book.number_of_pages) / Decimal('100.0')
            self.fees = fee_per_month * months_overdue
        else:
            self.fees = Decimal('0.00')
        self.save()

    def __str__(self):
        return f"{self.user.username} rented '{self.book.title}'"
