from django.urls import path
from . import views
from .views import grant_wish

app_name = 'donations'

urlpatterns = [
    # Donation page
    path('donate/', views.DonateView.as_view(), name='donate'),
    
    # Donor dashboard
    path('dashboard/', views.DonorDashboardView.as_view(), name='dashboard'),
    
    # Grant wish
    path('grant/<int:wish_id>/', grant_wish, name='grant_wish'),
]
