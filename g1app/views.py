from django.shortcuts import render, redirect, get_object_or_404
                                                                                                                                                                                                
import random
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password


from .models import User, Article, Video, Race, RaceResult, PasswordResetOTP
from django.contrib.auth.models import User
from django.conf import settings





# ------------------ INDEX PAGE (Articles) ------------------

def index(request):
    featured = Article.objects.filter(is_featured=True).first()
    sidebar_articles = Article.objects.filter(is_featured=False).order_by('-created_at')[:6]
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

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('Register_page')

        User.objects.create_user(
            username=email,        # email used as username
            email=email,
            password=password,
            first_name=fullname
        )

        messages.success(request, "Registration successful. Please sign in.")
        return redirect('Register_signIn')

    return render(request, 'g1app/register.html')


def Register_signIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,    # MUST match register username
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'g1app/signin.html')





def logout_user(request):
    request.session.flush()
    return redirect('index')


# ------------------ FORGOT / RESET PASSWORD ------------------




# ------------------ FORGOT PASSWORD ------------------

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect("forgot_password")

        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
            "Your OTP for Password Reset",
            f"Your OTP is: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        request.session["reset_user_id"] = user.id
        return redirect("verify_otp")

    return render(request, "g1app/forgot_password.html")






def verify_otp(request):
    user_id = request.session.get("reset_user_id")
    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)   # ✅ FIXED

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

    user = User.objects.get(id=user_id)   # ✅ FIXED

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        user.password = make_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully. Please login.")
        return redirect("Register_signIn")

    return render(request, "g1app/reset_password.html")








# ------------------ ARTICLE DETAILS PAGE ------------------



def article_detail(request, slug, category=None):
    article = get_object_or_404(Article, slug=slug)

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
