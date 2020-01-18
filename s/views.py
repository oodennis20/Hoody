from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            current_user.is_active = False
            current_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Hoods account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token':account_activation_token.make_token(current_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        current_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        current_user = None
    if current_user is not None and account_activation_token.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()
        login(request, current_user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. <a href="https://Hoodies.herokuapp.com"> Login </a> Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def home(request):
    profile = Profile.get_profile()
    business = Business.get_business()

    hoods= Hood.get_hoods()

    return render(request,"home.html",{"hoods":hoods, "business":business,"profile":profile})

def new_business(request):
    current_user = request.user

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.save()
            return redirect('neighbourhood')

    else:
        form = BusinessForm()
    return render(request, 'business.html', {"form": form})

@login_required(login_url='/accounts/login')
def profile(request):

    profile = Profile.objects.get(user = request.user)

    return render(request,"profiles/profile.html",{"profile":profile})    

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES,instance = profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.email = current_user.email
            profile.save()
        return redirect('profile')

    else:
        form = EditProfileForm(instance = profile)
    return render(request, 'profiles/edit_profile.html', {"form": form})

@login_required(login_url="/accounts/login/")
def join(request,operation,pk):
    hood = get_object_or_404(Hood,pk=pk)

    if operation == 'join':
        hood.join += 1
        hood.save()
        return render(request, "hood.html", {"hood":hood})
    elif operation =='unjoin':
        hood.join -= 1
        hood.save()
    return redirect('home')

