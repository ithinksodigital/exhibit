from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm, MsgForm, NewsletterForm, InMailForm
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def index(request):
    username = None
    try:
        if request.user.is_authenticated:
            username = request.user.username
    except: pass
    photos = Photo.objects.all().order_by('-photo_like')

    context = {'photos' : photos,
               'username': username}
    return render(request, 'exhibit/index.html', context)


def user(request, username):
    user = User.objects.get(username=username)
    photos = Photo.objects.filter(owner=user.pk)
    context = {'photos' : photos}
    return render(request, 'exhibit/user_p.html', context)
    # u = User.objects.all()
    # return HttpResponse(u)

@login_required
def me(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        photos = Photo.objects.filter(owner=user.pk)
        context = {'photos': photos,
                  'username': username}
        return render(request, 'exhibit/user_p.html', context)
    else:
        return render(request, 'exhibit/notlogin.html')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'exhibit/signup.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, "exhibit/login.html", {"form":form})
        else:
            return render(request, "exhibit/login.html", {"form": form})
    form = AuthenticationForm()
    return render(request, "exhibit/login.html", {"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")

@login_required
def photo_add(request):
    if request.user.is_authenticated:
        username= None
        username = request.user.username
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                if request.user.is_authenticated:
                    username = request.user.username
                    user = User.objects.get(username=username)
                    photo.owner = user
                photo.save()
                # return redirect('post_detail', pk=photo.pk)
                return redirect('me')
        else:
            form = PostForm()
        return render(request, 'exhibit/add_photo.html', {'form': form, 'username': username})
    else:
        return render(request, 'exhibit/notlogin.html')


def search(request):
    username = None
    try:
        if request.user.is_authenticated:
            username = request.user.username
    except:
        pass
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__contains=query)
        photos = Photo.objects.filter(photo_title__contains=query)
        context = {'users': users, 'photos': photos, 'username': username}
        return render(request, 'exhibit/results.html', context )
    else:
        return render(request, 'exhibit/results.html', context={'empty':'empty'})

@login_required
def follow(request):
    if request.user.is_authenticated:

        f = request.GET.get('f')
        user_to_follow = User.objects.get(pk=f)
        if request.user.is_authenticated:
            username = request.user.username
            user_from = User.objects.get(username=username)
        c = Contact( user_from=user_from, user_to=user_to_follow)
        c.save()

        return redirect('contacts')
    else:
        return render(request, 'exhibit/notlogin.html')
@login_required
def contacts(request):
    if request.user.is_authenticated:
        username = request.user.username
        user_from = User.objects.get(username=username)
        q = Contact.objects.filter(user_from=user_from)
        context = {'contacts': q, 'username': username}
        return render(request, 'exhibit/contacts.html', context)
    else:
        return render(request, 'exhibit/notlogin.html')

@login_required
def send_message(request):
    if request.user.is_authenticated:
        username= None
        username = request.user.username
        if request.method == "POST":
            form = MsgForm(request.POST, request.FILES)
            if form.is_valid():
                msg = form.save(commit=False)
                if request.user.is_authenticated:
                    username = request.user.username
                    user = User.objects.get(username=username)
                    msg.userfrom = user
                    subject = form.cleaned_data['msgtitle']
                    from_email = form.cleaned_data['useremail']
                    msg_to_send = "Wiadomość od: " + from_email + " treść: " + form.cleaned_data['msg']
                    message = msg_to_send
                    msg.save()
                    try:
                        send_mail(subject, message, from_email, ['czesc@ithinkso.pl'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return render(request, 'exhibit/success.html',{'form': form, 'username': username} )
                return render(request, 'exhibit/success.html',{'form': form, 'username': username} )

                msg.save()
                # return redirect('post_detail', pk=photo.pk)
                return render(request, 'exhibit/success.html',{'form': form, 'username': username} )
        else:
            form = MsgForm()
        return render(request, 'exhibit/contact_form.html', {'form': form, 'username': username})
    else:
        return render(request, 'exhibit/notlogin.html')

@login_required
def newsletter(request):
    if request.user.is_authenticated:

        username = None
        username = request.user.username
        if request.method == "POST":
            form = NewsletterForm(request.POST)
            rodo = request.POST.get('rodo', '')
            print('log')
            print(rodo)
            if rodo == '':
                return render(request, 'exhibit/bad.html', {'form':form, 'username':username})
            if form.is_valid():
                newsletter = form.save(commit=False)
                if request.user.is_authenticated:
                    username = request.user.username
                    user = User.objects.get(username=username)
                    newsletter.user = user
                newsletter.save()
                # return redirect('post_detail', pk=photo.pk)
                return render(request, 'exhibit/success.html')
        else:
            form = NewsletterForm()
        return render(request, 'exhibit/newsletter.html', {'form': form, 'username': username})
    else:
        return render(request, 'exhibit/notlogin.html')

@login_required
def inmails(request):
    if request.user.is_authenticated:
        username = None
        username = request.user.username
        username_getpk = User.objects.get(username=username)
        inmails = InMail.objects.filter(to_user=username_getpk)
        if request.method == "POST":
            form = InMailForm(request.POST)
            if form.is_valid():
                inmail = form.save(commit=False)
                if request.user.is_authenticated:
                    username = request.user.username
                    user = User.objects.get(username=username)
                    inmail.from_user = user
                inmail.save()
                return render(request, 'exhibit/inmail.html', {'form': form, 'username': username, 'inmails': inmails, 'success':True, 'username': username})
        else:
            form = InMailForm()
        return render(request, 'exhibit/inmail.html', {'form': form, 'username': username, 'inmails':inmails})
    else:
        return render(request, 'exhibit/notlogin.html')

@login_required
def inmail(request, inmail_id):
    if request.user.is_authenticated:
        try:
            username = None
            inmail_id = inmail_id
            username = request.user.username
            username_getpk = User.objects.get(username=username)
            inmails = InMail.objects.filter(to_user=username_getpk)
            inmail = InMail.objects.get(id=inmail_id, to_user=username_getpk)

            return render(request, 'exhibit/inmail_.html', {'username': username, 'inmail': inmail, 'inmails':inmails})
        except InMail.DoesNotExist:
            username = None
            username = request.user.username
            username_getpk = User.objects.get(username=username)
            inmails = InMail.objects.filter(to_user=username_getpk)
            DoesNotExist = ""
            if request.method == "POST":
                form = InMailForm(request.POST)
                if form.is_valid():
                    inmail = form.save(commit=False)
                    if request.user.is_authenticated:
                        username = request.user.username
                        user = User.objects.get(username=username)
                        inmail.from_user = user
                    inmail.save()
                    return render(request, 'exhibit/inmail.html',
                                  {'form': form, 'username': username, 'inmails': inmails, 'success': True,
                                   'username': username})
            else:
                form = InMailForm()
            return render(request, 'exhibit/inmail.html', {'form': form, 'username': username, 'inmails': inmails, 'DoesNotExist':True})

    else:
        return render(request, 'exhibit/notlogin.html')

@login_required
def detail(request, img_id):
    try:
        q = request.GET.get('q')
        img_id = img_id
        photo = Photo.objects.get(pk=img_id)
        liked = Vote.objects.filter(photo_vote=photo)
        liked = len(liked)
        context={'photo':photo,
                 'q':q, 'liked':liked}
        return render(request, 'exhibit/detail.html',context )
    except:
        pass

@login_required
def like(request, img_id):
    if request.user.is_authenticated:
        username = None
        username = request.user.username
        user = User.objects.get(username=username)
        photo = Photo.objects.get(pk=img_id)
        v = Vote.objects.filter(user_vote=user, photo_vote=photo)
        print('log!!!! ')
        print(v)
        if not v:
            v = Vote(user_vote=user, photo_vote=photo)
            v.save()
            back = '../detail/'+str(img_id)+'?q=success'
            return redirect(back)
        else:
             back = '../detail/'+str(img_id)+'?q=votebefore'
             return redirect(back)


