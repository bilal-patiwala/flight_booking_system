from .views import FlightUserLogin, FlightAdminLogin
from . import views
from django.urls import path


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('flight-user-login/', views.FlightUserLogin, name='flight_user_login'),
    path('flight-admin-login/',views.FlightAdminLogin, name="flight_admin_login"),
    path('flight-user-register/', views.flight_user_register, name="flight_user_register"),
    path('flight-admin-register/', views.flight_admin_register, name="flight_admin_register"),
    path('add-flight/',views.addflight, name="add_flight"),
    path('delete-flight/<str:id>/',views.deleteFlight, name="delete_flight"),
    path('book-ticket/',views.bookTicket, name="book_ticket"),
    path("get-flight/",views.getFlights, name="get_flight"),
    path("get-user-booked-tickets/", views.user_booked_tickets, name="user_booked_tickets"),
    path("get-flight-for-admin/",views.getFlightsForAdmin, name="get_flights_for_admin"),
    path("get-single-flight/", views.getsingleFlights)
]