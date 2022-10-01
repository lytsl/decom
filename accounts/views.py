from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from ecom import settings
from .forms import RegistrationForm
from .models import Account


# import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_num = form.cleaned_data['phone_num']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                name=name,
                username=username,
                email=email,
                password=password,
                # phone_num=phone_num
            )
            user.phone_num = phone_num
            # user.is_active = True
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account To Login!'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email_from = settings.EMAIL_HOST_USER
            send_email = EmailMessage(mail_subject, message, email_from, to=[to_email])
            send_email.send()

            messages.success(request, 'Verify your email to activate your account')
            return redirect('/auth/login/?command=verification&email=' + email)

            # messages.success(request, 'Created a new account. Log in to continue.')
            # return redirect('/auth/login/')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'auth/register.html', context=context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
        else:
            auth.login(request, user)
            return redirect('home')

    return render(request, 'auth/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully Logged Out!')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is Activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password.'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Email has been send to you, reset password!!')
            return redirect('login')

        else:
            messages.error(request, 'Account Does Not Exists..')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Email.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Invalid Validation Link.')
        return redirect('login')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Successfully Changed, Login.')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your Password was Updated Successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'You Entered A Wrong Password.')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords did not match.')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')


