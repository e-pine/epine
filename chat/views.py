from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
@login_required
def rooms(request):
    rooms = Room.objects.filter(slug="supplier")

    return render(request, 'chat/rooms.html', {'rooms':rooms})
@login_required
def room(request,slug):
    # rooms = Room.objects.all()
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'chat/room.html', {'room':room, 'messages': messages, })

def room_delete(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return redirect('index')
    
    if request.method == 'POST':
        room.delete()
        return redirect('index')
  
    return render(request, 'chat/room_delete.html', {'room': room})