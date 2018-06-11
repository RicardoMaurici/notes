from django.shortcuts import render, redirect, get_object_or_404,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Note

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mynotes'))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mynotes'))
        return render(request, 'app/login.html', {
            'error_message': "Email ou senha incorretos.",
        })
    return render(request, 'app/login.html')

def signup(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponseRedirect(reverse('login_user'))
    return render(request, 'app/signup.html')

@login_required(login_url='/login/')
def mynotes(request):
    userid = request.user.id
    user = get_object_or_404(User, pk=userid)
    notes = Note.objects.filter(user = user,active=True)
    context = notes
    return render(request, 'app/mynotes.html', {'notes': context})

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_user'))

@login_required(login_url='/login/')
def newnote(request):
    if request.POST:
        userid = request.user.id
        titulo = request.POST['titulo']
        texto = request.POST['texto']
        user = get_object_or_404(User, pk=userid)
        note = Note(title = titulo,text=texto,user=user)
        note.save()
        return HttpResponseRedirect(reverse('mynotes'))
    return render(request, 'app/new_note.html')

@login_required(login_url='/login/')
def edit(request,note=None):
    if request.POST:
        note_id = request.POST.get('remove_note_id', 0)
        if note_id:
            n = get_object_or_404(Note, pk=note_id)
            n.active = False
            n.save()
        else:
            print(request.POST)
            titulo = request.POST['titulo']
            texto = request.POST['texto']
            note_id = request.POST['note_id']
            n = get_object_or_404(Note, pk=note_id)
            n.title = titulo
            n.text = texto
            n.save()
        return HttpResponseRedirect(reverse('mynotes'))
    n = get_object_or_404(Note, pk=note)
    return render(request, 'app/update.html', {'note': n})