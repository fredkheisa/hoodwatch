from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, CreateHoodForm, CreateBizForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Neighbour, Profile, Join

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
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
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('landing')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='/accounts/login/')
def index(request):
    """
    Renders the index page
    """
    if Join.objects.filter(user_id = request.user).exists():
        hood = Neighbour.objects.get(pk = request.user.join.hood_id)
        return render(request,'hood.html', locals())

    else:
        hoods = Neighbour.objects.all()
    return (request, 'index.html', locals())


@login_required(login_url='/accounts/login/')
def createhood(request):
    """
    Renders the creating hood form
    """
    if request.method == 'POST':
        form = CreateHoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit = False)
            hood.user = request.user
            hood.save()
            return redirect('landing')
    else:
        form = CreateHoodForm()
        return render(request, 'forms/hood.html', {"form":form})


@login_required(login_url='/accounts/login/')
def edithood(request , id):
    """
    This view edits neighbour class
    """
    neighbour = Neighbour.objects.get(pk = id)
    if request.method == 'POST':
        form = CreateHoodForm(request.POST,instance = neighbour)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = request.user
            hood.save()
        return redirect('landing')
    else:
        form = CreateHoodForm(instance = neighbour)
    return render(request, 'edit/hood.html', locals())


@login_required(login_url='/accounts/login/')
def delhood(request , id):
    """
    View function that deleted a hood
    """
    Neighbour.objects.filter(pk = id).delete()
    return redirect('landing')

@login_required(login_url='/accounts/login/')
def join(request , hoodid):
    """
    This view edits neighbour class
    """
    this_hood = Neighbour.objects.get(pk = hoodid)
    if Join.objects.filter(user = request.user).exists():
        Join.objects.filter(user_id = request.user).update(hood_id = this_hood.id)
    else:
        Join(user=request.user, hood_id = this_hood.id).save()
    messages.success(request, 'Success! You have succesfully joined this Neighbourhood ')
    return redirect('landing')


@login_required(login_url='/accounts/login/')
def createbiz(request):
    """
    Creates business class
    """
    if Join.objects.filter(user_id = request.user).exists():
        if request.method == 'POST':
            form = CreateBizForm(request.POST)
            if form.is_valid():
                business = form.save(commit = False)
                business.user = request.user
                business.hood = request.user.join.hood_id
                business.save()
                messages.success(request, 'Success! You have created a business')
                return redirect('allBusinesses')
        else:
            form = CreateBizForm()
            return render(request, 'forms/biz.html',{"form":form})
    else:
        messages.error(request, 'Error! Join a Neighbourhood to create a Business')




        




