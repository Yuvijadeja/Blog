import random
import smtplib
from datetime import date, datetime
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Attempts, Profile
from django.apps import apps

# Create your views here.
Blogs = apps.get_model('blogs', 'Blogs')


def cat_load():
    cat_design = Blogs.objects.filter(category="Designing").count()
    cat_script_lang = Blogs.objects.filter(category="Scripting-Language").count()
    cat_pro_lang = Blogs.objects.filter(category="Programming-Language").count()
    cat_tech = Blogs.objects.filter(category="Technology").count()
    cat_pro = Blogs.objects.filter(category="Programming").count()
    categories = [cat_design, cat_script_lang, cat_pro_lang, cat_tech, cat_pro]
    return categories


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        if User.objects.filter(email=username, is_active=0).exists():
            messages.warning(request, "Your account is blocked! Please contact webmaster")
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if Attempts.objects.filter(email=username).exists():
                    Attempts.objects.filter(email=username).delete()
                auth.login(request, user)
                return redirect('/')
            else:
                if User.objects.filter(email=username).exists():
                    current_time = datetime.now()
                    if Attempts.objects.filter(email=username).exists():
                        att = Attempts.objects.get(email=username)
                        update_att = att.attempts + 1
                        att_time = str(att.attempt_time)
                        fail_time = datetime.strptime(att_time, "%H:%M:%S")

                        fail_time_tup = fail_time.strftime("%H:%M").split(':')
                        current_time_tup = current_time.strftime("%H:%M").split(':')

                        hour = int(current_time_tup[0]) - int(fail_time_tup[0])
                        minute = int(current_time_tup[1]) - int(fail_time_tup[1])

                        if minute < 0:
                            hour = hour - 1
                            minute = 60 + minute

                        if hour <= 2:
                            Attempts.objects.filter(email=username).update(attempts=update_att)
                            if update_att == 3:
                                User.objects.filter(email=username).update(is_active=0)
                        else:
                            Attempts.objects.filter(email=username).update(attempts=1,
                                                                           attempt_time=current_time.strftime("%H:%M"))
                    else:
                        attempt = Attempts.objects.create(email=username, attempts=1,
                                                          attempt_time=current_time.strftime("%H:%M"))
                        attempt.save()
                messages.info(request, "Invalid Username or Password!")

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully logout!")
    return redirect('login')


def signup(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        today = date.today()

        if User.objects.filter(email=email).exists():
            messages.warning(request, "This email id is already registered with us!")
        else:
            user = User.objects.create_user(first_name=fname, last_name=lname,
                                            username=email, email=email, password=password)
            user.save()

            Profile.objects.create(firstname=fname, last_name=lname, email=email, dob=dob, gender=gender, date_join=today)

            messages.info(request, "Hurray! You are registered with us.")

    return render(request, 'signup.html')


def account(request):
    if request.user.is_authenticated:
        user_obj = request.user
        user = Profile.objects.filter(email=user_obj.username).get()
        pro = Profile.objects.get(email=user_obj.username)
        blogs = Blogs.objects.filter(creator=user_obj.username).all()
        if not blogs:
            messages.info(request, "No blogs found!")
            return render(request, 'account.html', {'categories': cat_load(), 'user': user})
        else:
            page = request.GET.get('page', 1)

            try:
                record = 1 * int(page)
                count = Blogs.objects.filter(creator=user_obj.username).count()
                page_num = 1 + int(page)
                if page_num > count:
                    page_num = 0
                blog = Blogs.objects.filter(creator=user_obj.username).all()[0:record]
                return render(request, 'account.html', {'categories': cat_load(), 'profile': pro,
                                                        'blogs': blog, 'pageNo': page_num})
            except:
                raise Http404("Invalid Page Number!")
    else:
        return redirect('login')


def profile(request, username):
    pro = Profile.objects.get(email=username)
    blogs = Blogs.objects.filter(creator=username).all()
    if not blogs:
        messages.info(request, "No blogs found!")
        return render(request, 'profile.html', {'categories': cat_load(), 'profile': pro})
    else:
        page = request.GET.get('page', 1)

        try:
            record = 1 * int(page)
            count = Blogs.objects.filter(creator=username).count()
            page_num = 1 + int(page)
            if page_num > count:
                page_num = 0
            blog = Blogs.objects.filter(creator=username).all()[0:record]
            return render(request, 'profile.html', {'categories': cat_load(), 'profile': pro,
                                                    'blogs': blog, 'pageNo': page_num})
        except:
            raise Http404("Invalid Page Number!")


def update_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            email = request.POST.get('email')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            print(email)
            User.objects.filter(username=email).update(first_name=first_name, last_name=last_name)
            Profile.objects.filter(email=email).update(first_name=first_name, last_name=last_name, dob=dob,
                                                       gender=gender)
            messages.info(request, "Account Updated Successfully!")
            return redirect('account')
    else:
        return redirect('login')


def change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            old_pass = request.POST.get('oldpass')
            new_pass = request.POST.get('newpass')
            username = request.user.username
            user = auth.authenticate(username=username, password=old_pass)
            if user is not None:
                u = User.objects.get(username=username)
                u.set_password(new_pass)
                u.save()
                messages.info(request, "Password Changed!")
                auth.logout(request)
                return redirect('login')
            else:
                messages.info(request, "Password does not match!")
                return redirect('account')
        else:
            return redirect('account')
    else:
        return redirect('login')


def forgot_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
            p = "".join(random.sample(s, 8))
            print(p)
            sender = 'info.appsoftsolution@gmail.com'
            receiver = email
            message = """From: TechBlog
                        Subject: New Password for TechBlog account.

                        Hi!
                        You are registered at TechBlog.
                        Your Password is: """ + p

            def send(receive):
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.starttls()
                mail.login(sender, '@pps0ft1993')
                mail.sendmail(sender, receive, message)

            # send(receiver)

            messages.info(request, "New password send to your email address!")
            return redirect('login')
        else:
            messages.warning(request, email + " is not registered with us!")
