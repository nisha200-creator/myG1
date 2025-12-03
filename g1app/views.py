from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

from .models import UserTable, PasswordResetToken, Article


# ------------------ INDEX PAGE (Articles) ------------------

def index(request):
    featured = Article.objects.filter(is_featured=True).first()
    sidebar_articles = Article.objects.filter(is_featured=False).order_by('-created_at')[:5]

    return render(request, 'g1app/index.html', {
        'featured': featured,
        'sidebar_articles': sidebar_articles,
    })


# ------------------ STATIC PAGES ------------------

def news(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, "g1app/news.html", {"articles": articles})


def teams(request):
    return render(request, 'g1app/Teams.html')

def about(request):
    return render(request, 'g1app/about.html')

def schedule(request):
    return render(request, 'g1app/schedule.html')


# ------------------ SIGNIN / REGISTER ------------------

users = {}   # temporary memory user

def Register_page(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        users[email] = {
            'name': fullname,
            'password': password
        }

        return redirect('Register_signIn')

    return render(request, 'g1app/register.html')


def Register_signIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email in users and users[email]['password'] == password:
            request.session['user_email'] = email
            request.session['user_name'] = users[email]['name']
            return redirect('index')

        return render(request, 'g1app/signin.html', {'error': "Invalid email or password"})

    return render(request, 'g1app/signin.html')


def logout_user(request):
    request.session.flush()
    return redirect('index')


# ------------------ FORGOT / RESET PASSWORD ------------------

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not UserTable.objects.filter(email=email).exists():
            messages.error(request, "No account found with this email.")
            return redirect('forgot_password')

        token = get_random_string(64)
        PasswordResetToken.objects.create(email=email, token=token)

        reset_link = request.build_absolute_uri(f"/reset-password/{token}/")

        send_mail(
            "Reset Your Password",
            f"Click the link to reset your password: {reset_link}",
            "noreply@example.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "Reset link sent to your email.")
        return redirect('Register_signIn')

    return render(request, "g1app/forgot_password.html")


def reset_password(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
    except:
        messages.error(request, "Invalid or expired link.")
        return redirect('Register_signIn')

    if timezone.now() - token_obj.created_at > timedelta(minutes=30):
        token_obj.delete()
        messages.error(request, "Link expired.")
        return redirect('forgot_password')

    if request.method == "POST":
        new_pass = request.POST.get("password")
        c_pass = request.POST.get("cpassword")

        if new_pass != c_pass:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        user = UserTable.objects.get(email=token_obj.email)
        user.password = new_pass
        user.save()

        token_obj.delete()

        messages.success(request, "Password updated successfully.")
        return redirect('Register_signIn')

    return render(request, "g1app/reset_password.html")


# ------------------ ARTICLE DETAILS PAGE ------------------

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    return render(request, 'g1app/article_details.html', {
        'article': article
    })
