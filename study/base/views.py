from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q


def home(request):
    topic_name = request.GET.get('topic')  
    q = request.GET.get('q')  # Get search query from URL parameter
    
    # Start with all rooms
    query = Room.objects.all()
    
    # Filter by topic if specified
    if topic_name:
        query = query.filter(topic__name=topic_name)
    
    # Filter by search query if specified
    if q:
        query = query.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(topic__name__icontains=q)
        )
    
    topics = Topic.objects.all()
    context = {
        'query': query,
        'topics': topics,
        'selected_topic': topic_name,
    }
    return render(request, 'home.html', context)

def room(request, pk):  
    query = get_object_or_404(Room, id=pk)
    messages = query.message_set.all().order_by('-created')[:50]
    context = {
        'room': query, 
        'messages':messages
    }
    return render(request, 'room.html', context)

def create_room(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={
        'form':form
    }
    return render(request, 'create_room.html',context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form= RoomForm(instance=room)
    context = {'form' :form}
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'create_room.html', context)

def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render (request, 'delete.html',{'obj':room})
