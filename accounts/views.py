from django.shortcuts import render, redirect
from django import forms
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, authenticate


from .forms import RegisterForm
from .models import Account

# Create your views here.


def register(request):
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
            )

            # Account Activation Mail
            domain = get_current_site(request).domain
            mail_subject = "Please activate you registered account!"
            mail_context = {
                "domain": domain,
                "user": user,
                "encoded_user_id": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            mail_body = render_to_string(
                "accounts/account_activation_mail.html", mail_context
            )
            mail = EmailMessage(mail_subject, mail_body, to=[email])

            try:
                mail.send()
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
