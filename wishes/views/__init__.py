# Import views to make them available when importing from wishes.views
from .create_wish import CreateWishView
from .dashboard import WishDashboardView

__all__ = [
    'CreateWishView',
    'WishDashboardView'
]