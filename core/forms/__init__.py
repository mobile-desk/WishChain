# This file makes the forms directory a Python package
# Import forms here to make them available at core.forms
from .auth_forms import (
    BaseRegistrationForm,
    DonorRegistrationForm,
    WisherRegistrationForm,
    UserLoginForm
)

__all__ = [
    'BaseRegistrationForm',
    'DonorRegistrationForm',
    'WisherRegistrationForm',
    'UserLoginForm'
]
