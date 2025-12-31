from django.urls import path
from .views import resend_verification_view

urlpatterns = [
    path('resend-email/', resend_verification_view, name='resend_verification'),
]
