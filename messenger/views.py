import datetime
from itertools import chain

from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .models import Message
from .forms import FindUsers
from website.models import *


class MessengerView(TemplateView):
    template_name = 'messenger/messenger.html'
    find_form = FindUsers

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context)

    @login_required
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)


        return HttpResponseRedirect(reverse('messenger:messenger'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter()



@login_required
def messenger(request):
    context = {}
    user = request.user
    friends = user.friends.all()
    context['profile'] = profile
    context['friends'] = friends
    context['recipient'] = None
    context['find_users'] = FindUsers()
    context['search_results'] = []
    if request.method == 'GET':
        if 'find_users' in str(request.GET):
            find_form = FindUsers(request.GET)
            if find_form.is_valid():
                form_data = find_form.cleaned_data
                name = form_data['name']
                context['search_results'] = MyUser.objects.filter(username__icontains=name)
                print(context['search_results'])
            else:
                print(f'error {find_form.errors}')
    else:
        friend = MyUser.objects.get(user=MyUser.objects.get(id=request.POST['add_friend']))
        if not user.friends.filter(user=friend).exists():
            user.friends.add(friend)

    return render(request, 'messenger/messenger.html', context)


@login_required
def chat(request, friend_id):
    context = {}
    user = request.user
    friends = user.friends.all()
    recipient = MyUser.objects.get(id=friend_id)
    context['profile'] = user
    context['friends'] = friends
    context['recipient'] = recipient
    context['find_users'] = FindUsers()
    context['search_results'] = []
    sent_msgs = Message.objects.filter(sender=user, recipient=recipient)
    received_msgs = Message.objects.filter(sender=recipient, recipient=user)
    msgs = sorted(
        chain(sent_msgs, received_msgs),
        key=lambda instance: instance.timestamp)
    context['messages'] = msgs
    return render(request, 'messenger/chat.html', context)


def get_messages(request, friend_id):
    user = request.user
    recipient = MyUser.objects.get(id=friend_id)
    sent_msgs = Message.objects.filter(sender=user, recipient=recipient).values()
    received_msgs = Message.objects.filter(sender=recipient, recipient=user).values()
    msgs = sorted(
        chain(sent_msgs, received_msgs),
        key=lambda instance: instance['timestamp'])
    for msg in msgs:
        msg['sender_id'] = MyUser.objects.get(id=msg['sender_id']).username
    return JsonResponse({'messages': msgs})


def send(request):
    sender = request.user.profile
    recipient = MyUser.objects.get(id=request.POST['recipient_id'])
    message = request.POST['msg_text']
    date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
    Message.objects.create(sender=sender, recipient=recipient, content=message, timestamp=date)
    return HttpResponse('sent')





