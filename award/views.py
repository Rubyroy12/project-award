from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from .forms import ProfileForm,UpdateUserForm,UpdateUserProfileForm,ProjectForm,RatingForm
from .models import Project,Rating

# Create your views here.

def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html',{"projects":projects})

@login_required(login_url='/accounts/login/')
def profile(request, username):
    images = request.user.profile.images.all()
    print(images)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        'images': images,
    }
    return render(request, 'profile.html', params)


@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('profile')
    else:
        form = ProjectForm()
    return render(request,'edit_profile.html',{"form":form})

@login_required(login_url='/accounts/login/')
def submit(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            submit = form.save(commit=False)
            submit.user = request.user.profile
            submit.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request,'submit.html', {"form":form})

    
def project(request,id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form= RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
        rates=Rating.objects.all()
  
    return render(request,'project.html',{"project":project, "form":form,"rates":rates})
