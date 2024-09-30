# rentals/urls.py

from django.urls import path
from . import views

app_name = 'rental'

urlpatterns = [
    path('start/', views.StartRentalView.as_view(), name='start_rental'),
    path('extend/', views.ExtendRentalView.as_view(), name='extend_rental'),
    path('rental/<int:pk>/', views.RentalDetailView.as_view(), name='rental_detail'),
    path('dashboard/<int:user_id>/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('confirm_start/<int:pk>/', views.RentalConfirmStartView.as_view(), name='rental_confirm_start'),
    path('confirm_extend/<int:pk>/', views.RentalConfirmExtendView.as_view(), name='rental_confirm_extend'),
]
