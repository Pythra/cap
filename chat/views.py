from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import MessageForm
from .models import Message


def index(request):
    chats = User.objects.all
    return render(request, 'chat/index.html', {'chats': chats})


@login_required
def room(request, room_name):
    meg = Message.objects.filter(user2=request.user)
    meg.update(status='seen')
    me = request.user
    if request.user.is_superuser:
        other = User.objects.get(id=room_name)
    else:
        other = User.objects.get(id=1)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user1 = me
            message.user2 = other
            message.save()
    else:
        form = MessageForm()
    messages = Message.objects.filter(Q(user1=me, user2=other) | Q(user1=other, user2=me)).order_by('created_on')[7:]
    paginator = Paginator(messages, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'chat/room.html', {
        'room_name': room_name, 'page_obj': page_obj,
        'messages': messages, 'form': form, 'other': other,
    })
