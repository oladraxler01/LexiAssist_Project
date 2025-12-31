from django.shortcuts import render, redirect

def resend_verification_view(request):
    # For now, just redirect back to the verification page
    # Later, you will add the logic to actually send the email here
    return redirect('verification')
