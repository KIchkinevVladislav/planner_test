from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Group
from django.urls import reverse



def home(request):
	"""
	Renders the home page with a list of chats.
	"""
	groups = Group.objects.all()
	return render(request, 'chat/home.html', {'groups':groups})


@login_required
def new_group(request):
	"""
	View for creating a new group chat.
	"""
	u = request.user
	new = Group.objects.create()
	new.members.add(u)
	new.save()
	return redirect(reverse('chat:home'))


@login_required
def join_group(request, uuid):
	"""
	View for joining a group chat new user.
	"""
	u = request.user
	gp = Group.objects.get(uuid=uuid)
	gp.members.add(u)
	gp.save()
	return redirect(reverse('chat:home'))


@login_required
def leave_group(request, uuid):
	"""
	View for leave a group chat.
	"""
	u = request.user
	gp = Group.objects.get(uuid=uuid)
	gp.members.remove(u)
	gp.save()
	return redirect(reverse('chat:home'))


@login_required
def open_chat(request, uuid):
    """
    View for opening a chat with a specific group identified by its UUID.

    Returns:
    - If the user is a member of the group, renders the chat page with sorted messages.
    - If the user is not a member, returns a forbidden response.
    """
    group = Group.objects.get(uuid=uuid)
    if request.user not in group.members.all():
        return HttpResponseForbidden('Вы не участник. Попробуйте другой чат')
    messages = group.message_set.all()
    sorted_messages = sorted(messages, key=lambda x: x.timestamp)
    return render(request, 'chat/chat.html', context={'messages':sorted_messages, 'uuid': uuid})


@login_required
def remove_group(request, uuid):
    """
    View for delete a group chat. 
	The link to the view in the template 
	is only available to the administrator.
    """
    Group.objects.get(uuid=uuid).delete()
    return redirect(reverse('chat:home'))