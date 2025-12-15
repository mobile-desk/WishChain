from django.urls import path
from .views import CreateWishView, WishDashboardView

app_name = 'wishes'

urlpatterns = [
    # Wish creation
    path('wish/create/', CreateWishView.as_view(), name='create_wish'),
    
    # Wish dashboard
    path('dashboard/', WishDashboardView.as_view(), name='dashboard'),
    
    # Add other wish-related URLs here
]
