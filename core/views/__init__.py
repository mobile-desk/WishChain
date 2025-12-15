from .home import HomeView
from .auth_views import LoginView, RegisterView, logout_view, profile
from .registration.views import DonorRegisterView, WisherRegisterView, RegistrationTypeView

__all__ = [
    'HomeView',
    'LoginView',
    'RegisterView',
    'logout_view',
    'profile',
    'DonorRegisterView',
    'WisherRegisterView',
    'RegistrationTypeView'
]