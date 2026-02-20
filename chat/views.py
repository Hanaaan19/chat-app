from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .forms import RegistrationForm,EmailLoginForm
from .models import CustomUser, Message


def register_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            user.is_online = True
            user.last_seen = timezone.now()
            user.save()

            return redirect('user_list')

    else:
        form = RegistrationForm()

    return render(request, 'chat/register.html', {'form': form})


def login_view(request):

    form = EmailLoginForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)

        user.is_online = True
        user.last_seen = timezone.now()
        user.save()

        return redirect('user_list')

    return render(request, 'chat/login.html', {'form': form})


@login_required
def logout_view(request):

    user = request.user
    user.is_online = False
    user.last_seen = timezone.now()
    user.save()

    logout(request)
    return redirect('login')


@login_required
def user_list(request):

    users = CustomUser.objects.exclude(id=request.user.id)

    user_data = []

    for user in users:
        unread_count = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()

        user_data.append({
            'user': user,
            'unread_count': unread_count
        })

    return render(request, 'chat/user_list.html', {
        'user_data': user_data
    })


@login_required
def chat_view(request, user_id):

    other_user = get_object_or_404(CustomUser, id=user_id)

    room_name = f"{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}"

    
    unread = Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    )

    ids = list(unread.values_list("id", flat=True))
    unread.update(is_read=True)

    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{room_name}",
        {
            "type": "read_status",
            "message_ids": ids
        }
    )

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(request, "chat/chat.html", {
        "other_user": other_user,
        "messages": messages,
        "room_name": room_name
    })