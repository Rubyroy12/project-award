from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from .forms import ProfileForm,UpdateUserForm,UpdateUserProfileForm,ProjectForm,RatingForm, CommentForm
from .models import Project,Rating,Profile,ProfileMerch,ProjectMerch
from django.shortcuts import render,redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import MerchSerializer



# Create your views here.

def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html',{"projects":projects})

@login_required(login_url='/accounts/login/')
def profile(request, username):
    projects = request.user.profile.projects.all()
    
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
        'projects': projects,
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
        return redirect('/')
    else:
        form = ProjectForm()
    return render(request,'submit.html', {"form":form})

@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def comment(request, id):
    image = get_object_or_404(Project, pk=id)
    comments = image.comment.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = image
            comment.user = request.user.profile
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'image': image,
        'form': form,
        'comments':comments,
    }
    return render(request, 'post.html', params)

@login_required(login_url='/accounts/login/')
def search_project(request):
    if 'search_project' in request.GET and request.GET['search_project']:
        search_term = request.GET.get("search_project")
        results = Project.search_project(search_term)
        print(results)
        message = f'search_term'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You did not make a selection"
    return render(request, 'results.html', {'message': message})

    
class MerchProfileList(APIView):
    def get(self, request,format=None):
        all_merch = ProfileMerch.objects.all()
        serializers= MerchSerializer(all_merch,many=True)
        return Response(serializers.data)

class MerchProjectList(APIView):
    def get(self, request,format=None):
        all_merch = ProjectMerch.objects.all()
        serializers= MerchSerializer(all_merch,many=True)
        return Response(serializers.data)
