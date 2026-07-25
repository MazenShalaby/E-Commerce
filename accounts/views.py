from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, logout, authenticate


from .forms import RegisterForm
from .models import Account

# Create your views here.


def register(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = RegisterForm(request.POST, files=request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = Account.objects.create_user(
                email=email,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                age=form.cleaned_data.get("age"),
                gender=form.cleaned_data.get("gender"),
                profile_picture=form.cleaned_data.get("profile_picture"),
                password=form.cleaned_data.get("password"),
            )

            # Account Activation Mail
            domain = get_current_site(request).domain
            mail_subject = "Please activate you registered account!"
            mail_context = {
                "domain": domain,
                "user": user,
                "encoded_user_id": urlsafe_base64_encode(force_bytes(user.pk)),
                "generated_token": default_token_generator.make_token(user),
            }
            mail_body = render_to_string(
                "accounts/account_activation_mail.html", mail_context
            )
            mail = EmailMessage(mail_subject, mail_body, to=[email])

            try:
                mail.send()
                return redirect('login' + f"?command=activation&email={email}")
            except:
                user.delete()
                raise ValueError("Faild to send activation mail!")
        else:
            raise forms.ValidationError(
                "Something went wrong durring account registration!"
            )
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    
    return render(request, 'accounts/login.html', context={})


def logout_view(request):
    logout(request)
    return redirect('login')


def activate_registered_account(request, user_id_64, token):
    user_id = urlsafe_base64_decode(user_id_64).decode()
    user = get_object_or_404(Account, pk=user_id)
    if (user is not None) and (default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')