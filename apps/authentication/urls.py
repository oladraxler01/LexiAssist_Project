from django.urls import path
from django.contrib.auth import views as auth_views
# Add resend_verification and activate_account to this list
from .views import (
    signup_view,
    login_view,
    verification_view,
    resend_verification,
    activate_account
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    # Keep only one verification path
    path('verify/', verification_view, name='verification'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Removed "views." prefix since we imported the functions directly
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),


    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]
