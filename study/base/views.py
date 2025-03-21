from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def loginpage(request):
    page='login'
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
    try: 
        user=User.objects.get(username=username)
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    except:
        messages.error(request, 'User does not exist')
    context={'page':page}
    return render(request, 'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login_register.html',{'form':form})


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
    room_obj = get_object_or_404(Room, id=pk)
    room_messages = room_obj.message_set.all().order_by('-created')[:50]
    participants = room_obj.participants.all()
    
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room_obj,
            body=request.POST.get('body')
        )
        room_obj.participants.add(request.user)
        return redirect('room_detail', pk=room_obj.id)
       
    context = {
        'room': room_obj, 
        'messages': room_messages,
        'participants': participants,
    }
    return render(request, 'room.html', context)
        
       
    context = {
        'room': query, 
        'messages':room_messages
    }
    return render(request, 'room.html', context)


@login_required(login_url='loginpage')
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


@login_required(login_url='loginpage')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    
    form= RoomForm(instance=room)
    context = {'form' :form}
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'create_room.html', context)


@login_required(login_url='loginpage')
def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render (request, 'delete.html',{'obj':room})

@login_required(login_url='loginpage')
def deletemessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    room_id=message.room.id
    message.delete()
    return redirect('room_detail', pk=room_id)

def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    rooms = Room.objects.filter(host=user)
    room_messages = Message.objects.filter(user=user)
    topics = Topic.objects.all()
    
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
    }
    return render(request, 'profile.html', context)



