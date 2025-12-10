from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import UserTable, Article, Video, Race, RaceResult




# ------------------ INDEX PAGE (Articles) ------------------

def index(request):
    featured = Article.objects.filter(is_featured=True).first()
    sidebar_articles = Article.objects.filter(is_featured=False).order_by('-created_at')[:5]
    videos = Video.objects.all().order_by('-created_at')[:10]

    return render(request, 'g1app/index.html', {
        'featured': featured,
        'sidebar_articles': sidebar_articles,
        'videos': videos,
    })


# ------------------ STATIC PAGES ------------------

def news(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, "g1app/news.html", {"articles": articles})


def teams(request):
    return render(request, 'g1app/Teams.html')

def about(request):
    return render(request, 'g1app/about.html')


# view for shedule page import race model

def schedule(request):
    races = Race.objects.all().order_by('-round_number')

    return render(request, 'g1app/schedule.html', {'races': races})


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

        try:
            user = UserTable.objects.get(email=email)
        except UserTable.DoesNotExist:
            return render(request, 'g1app/signin.html', {'error': "Invalid email or password"})

        if user.password != password:
            return render(request, 'g1app/signin.html', {'error': "Invalid email or password"})

        # Login success
        request.session['user_email'] = user.email
        request.session['user_name'] = user.name
        return redirect('index')

    return render(request, 'g1app/signin.html')



def logout_user(request):
    request.session.flush()
    return redirect('index')


# ------------------ FORGOT / RESET PASSWORD ------------------

import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import UserTable, PasswordResetOTP


# ------------------ FORGOT PASSWORD ------------------

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = UserTable.objects.get(email=email)
        except UserTable.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect('forgot_password')

        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(user=user, otp=otp)

        print("OTP FUNCTION REACHED:", otp)   # <-- ADD THIS

        send_mail(
            "Your OTP for Password Reset",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        # Store user ID in session
        request.session["reset_user_id"] = user.id

        return redirect("verify_otp")

    return render(request, "g1app/forgot_password.html")





def verify_otp(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    # Get user
    user = UserTable.objects.get(id=user_id)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        try:
            otp_obj = PasswordResetOTP.objects.filter(user=user).latest("created_at")
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, "OTP expired or not found")
            return redirect("forgot_password")

        if entered_otp == otp_obj.otp:
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "g1app/verify_otp.html")

def reset_password(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    # Get user
    user = UserTable.objects.get(id=user_id)

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        # Update password
        user.password = new_password
        user.save()

        messages.success(request, "Password reset successfully. Please login.")
        return redirect("Register_signIn")

    return render(request, "g1app/reset_password.html")







# ------------------ ARTICLE DETAILS PAGE ------------------

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    return render(request, 'g1app/article_details.html', {
        'article': article
    })



# race result page



def race_results(request):
    results = RaceResult.objects.all()
    return render(request, "g1app/Result.html", {"results": results})


# video details view
def video_detail(request, id):
    video = get_object_or_404(Video, id=id)
    videos = Video.objects.all().order_by('-created_at')[:10]   # same as index page

    return render(request, "g1app/video_detail.html", {
        "video": video,
        "videos": videos,
    })




# subscribe view
from django.shortcuts import render
from django.http import JsonResponse
from .models import Subscriber

def subscribe_page(request):
    return render(request, "g1app/subscribe.html")

def subscribe_save(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({"status": "exists", "msg": "Already subscribed"})

        Subscriber.objects.create(email=email)
        return JsonResponse({"status": "ok", "msg": "Subscription successful"})

    return JsonResponse({"status": "error", "msg": "Invalid request"})
