# rentals/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Book, Rental
from .forms import RentalForm, ExtendRentalForm
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
from decimal import Decimal


class StartRentalView(View):
    """
    View to handle starting a new rental.
    """

    template_name = 'rentals/rental_form.html'

    def get(self, request):
        form = RentalForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RentalForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            book_title = form.cleaned_data['book_title']

            # Fetch book details from OpenLibrary API
            response = requests.get('https://openlibrary.org/search.json', params={'title': book_title})
            if response.status_code == 200:
                data = response.json()
                if data['docs']:
                    book_data = data['docs'][0]
                    number_of_pages = book_data.get('number_of_pages_median') or book_data.get('number_of_pages_estimate') or 0
                    openlibrary_key = book_data.get('key')

                    # Check if book already exists
                    book, created = Book.objects.get_or_create(
                        openlibrary_key=openlibrary_key,
                        defaults={
                            'title': book_title,
                            'number_of_pages': number_of_pages,
                        }
                    )

                    # Create Rental
                    rental = Rental.objects.create(user=user, book=book)
                    messages.success(request, 'Rental started successfully.')
                    return redirect('rental:rental_confirm_start', pk=rental.pk)
                else:
                    messages.error(request, 'Book not found in OpenLibrary.')
            else:
                messages.error(request, 'Failed to fetch book details from OpenLibrary.')
        return render(request, self.template_name, {'form': form})


class ExtendRentalView(View):
    """
    View to handle extending an existing rental.
    """

    template_name = 'rentals/extend_rental_form.html'

    def get(self, request):
        form = ExtendRentalForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExtendRentalForm(request.POST)
        if form.is_valid():
            rental = form.cleaned_data['rental']
            rental.extended = True
            rental.calculate_fees()
            messages.success(request, 'Rental extended successfully.')
            return redirect('rental:rental_confirm_extend', pk=rental.pk)
        return render(request, self.template_name, {'form': form})


class RentalDetailView(View):
    """
    View to display rental details.
    """

    template_name = 'rentals/rental_detail.html'

    def get(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        rental.calculate_fees()
        return render(request, self.template_name, {'rental': rental})


class StudentDashboardView(View):
    """
    View to display a student's rental dashboard.
    """

    template_name = 'rentals/student_dashboard.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        rentals = user.rentals.all()
        for rental in rentals:
            rental.calculate_fees()
        return render(request, self.template_name, {'user': user, 'rentals': rentals})


class RentalConfirmStartView(View):
    """
    View to confirm the start of a rental.
    """

    template_name = 'rentals/rental_confirm_start.html'

    def get(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        return render(request, self.template_name, {'rental': rental})


class RentalConfirmExtendView(View):
    """
    View to confirm the extension of a rental.
    """

    template_name = 'rentals/rental_confirm_extend.html'

    def get(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        return render(request, self.template_name, {'rental': rental})
