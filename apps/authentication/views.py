from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import User # This is the custom user we discussed
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=name
        )
        user.is_active = False
        user.save()

        send_verification_email(request, user)

        # REMOVE login(request, user) FROM HERE
        # Just redirect them to the verification instruction page
        return redirect('verification')

    return render(request, 'signup.html')



def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(f"--- DEBUG: Testing User: {user.email} (ID: {uid}) ---")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("--- DEBUG: User not found ---")

    token_valid = default_token_generator.check_token(user, token)
    print(f"--- DEBUG: Is Token Valid? {token_valid} ---")

    if user is not None and token_valid:
        user.is_active = True
        user.save()
        print("--- DEBUG: Account Activated! ---")
        messages.success(request, "Account verified! You can now log in.")
        return redirect('login')
    else:
        print("--- DEBUG: Verification Failed - Sending to Invalid Page ---")
        return render(request, 'activation_invalid.html')



from django.contrib.auth import authenticate

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')




def verification_view(request):
    return render(request, 'verif.html')
# Create your views here.



def send_verification_email(request, user):
    # 1. Generate unique token and user ID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # 2. Build the link (e.g., http://127.0.0.1:8000/activate/...)
    domain = request.get_host()
    link = f"http://{domain}/api/auth/activate/{uid}/{token}/"

    # 3. Prepare the email content
    subject = "Verify your LexiAssist Account"
    message = f"Hi {user.username},\n\nPlease click the link below to verify your account:\n{link}"

    # 4. Send the actual email
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")



def resend_verification(request):
    if request.user.is_authenticated:
        send_verification_email(request, request.user)
        messages.success(request, "A new verification link has been sent.")
        return render(request, 'verif.html') # Fixed path to match your verification_view
    else:
        messages.error(request, "Please log in first.")
        return redirect('login')
