from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View, UpdateView, DeleteView

from .forms import UserRegisterForm, AnnouncementForm, PostForm, CommentForm, ProfileForm
from .models import Profile, Announcement, Comment, Reply, Post
from .tokens import account_activation_token
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from chat.models import Message


def index(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '8',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '43be9fd4-af5b-4dbe-9379-6f749d993f8d',
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        coins = response.json()['data']
    except ConnectionError as e:
        print(e)
        coins = "No response"

    ann = Announcement.objects.all
    posts = Post.objects.all
    unread = Message.objects.filter(status='unseen', user1=request.user)
    context = {'ann': ann, 'posts': posts, 'coins': coins, 'unread':unread}
    return render(request, 'capping/index.html', context)


class SignUpView(View):
    form_class = UserRegisterForm
    template_name = 'capping/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'Please Confirm your email to complete registration.')

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


def announcement_form(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = AnnouncementForm()
    context = {'form': form}
    return render(request, 'capping/announcement_form.html', context)


@login_required
def profile_form(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('home'))

    else:
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'p_form': profile_form
    }
    return render(request, 'capping/profile_form.html', context)


def post_list(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': posts, 'page_obj': page_obj}
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'posts': posts, 'page_obj': page_obj}
    return render(request, 'capping/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.visits = post.visits + 1
    post.save()
    comments = post.comments.order_by('-created_on')
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))
    else:
        form = CommentForm()
    context = {'form': form, 'post': post, 'slug': slug, 'comments': comments, 'visits': post.visits,
               }
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'form': form, 'post': post, 'slug': slug, 'comments': comments, 'visits': post.visits,
                   }
    return render(request, 'capping/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
    context = {'form': form}
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'form': form}
    return render(request, 'capping/post_form.html', context)


class PostUpdate(UpdateView, LoginRequiredMixin):
    template_name = 'capping/post_update.html'
    model = Post
    form_class = PostForm


class PostDelete(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('home')


@login_required
def settings(request):
    context = {}
    return render(request, 'capping/settings.html', context)


@login_required
def trade(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '9',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '43be9fd4-af5b-4dbe-9379-6f749d993f8d',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        coins = response.json()['data']
    except ConnectionError as e:
        coins = "No response"

    context = {'coins': coins}
    return render(request, 'capping/trade.html', context)
