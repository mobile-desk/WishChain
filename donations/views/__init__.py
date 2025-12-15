# Import views to make them available when importing from donations.views
from donations.views.donate import DonateView
from donations.views.dashboard import DonorDashboardView
from donations.views.grant_wish import grant_wish

__all__ = [
    'DonateView',
    'DonorDashboardView',
    'grant_wish'
]