# from typing_extensions import Required
from django.forms.fields import NullBooleanField
from django.http import request
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # block the logout user go back addnew/findpost/checkdetail
#from braces.views import (LoginRequiredMixin, PermissionRequiredMixin, SuccessURLRedirectListMixin)
from django.views.generic import (
    CreateView, 
    ListView, 
    DetailView,
    UpdateView,
    DeleteView
    ) ####listview of post#####
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import (
    StudentSignUpForm, TutorSignUpForm, SchoolSignUpForm, UserUpdateForm, 
    ProfileUpdateForm, 
    EduProfileUpdateForm, 
    CanTeachForm, 
    OtherInfoForm,
    studentEduStateForm,
    schoolProfileForm,
    classCreateForm,
    classUpdateForm,
)
from django.contrib.auth.forms import AuthenticationForm
from .models import User, PostClass, Profile, TutorUser
#####permission
from .decorators import school_required

def register(request):
    return render(request, 'users/register.html', {})

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '../templates/users/student_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'學生用戶，成功登記，歡迎！')
        return redirect('login')

class tutor_register(CreateView):
    model = User
    form_class = TutorSignUpForm
    template_name = '../templates/users/tutor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'導師用戶，成功登記，歡迎！')
        return redirect('login')

class school_register(CreateView):
    model = User
    form_class = SchoolSignUpForm
    template_name = '../templates/users/school_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'學校用戶，成功登記，歡迎！')
        return redirect('login')

# def login_required(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data = request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None :
#                 login(request,user)
#                 return render(request, 'login', {})
#             else:
#                 messages.error(request,"Invalid username or password")
#         else:
#                 messages.error(request,"Invalid username or password")

#     return render(request, 'users/login.html', context={'form':AuthenticationForm()})

@login_required
def profile(request):
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-default border-bottom'
    if request.method == 'POST':
        #if request.user.is_tutor:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profile)
            e_form = EduProfileUpdateForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profile)
            ct_form = CanTeachForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profile)
            o_form = OtherInfoForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profile)
            st_edu_form = studentEduStateForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profile)
            school_profile_form = schoolProfileForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profile)
            if request.user.is_tutor and u_form.is_valid() and p_form.is_valid() and e_form.is_valid() and ct_form.is_valid() and o_form.is_valid():
                u_form.save()
                p_form.save()
                e_form.save()
                ct_form.save()
                o_form.save()
                messages.success(request, f'成功')
                return redirect('profile')
            elif request.user.is_student and u_form.is_valid() and p_form.is_valid() and st_edu_form.is_valid():
                u_form.save()
                p_form.save()
                st_edu_form.save()
                messages.success(request, f'成功')
                return redirect('profile')
            elif request.user.is_school and u_form.is_valid() and school_profile_form.is_valid():
                u_form.save()
                school_profile_form.save()
                messages.success(request, f'成功')
                return redirect('profile')

            ''' answer and st_edu_form.is_valid():
            if u_form.is_valid() and p_form.is_valid() and e_form.is_valid() and ct_form.is_valid() and o_form.is_valid() and st_edu_form.is_valid():
                u_form.save()
                p_form.save()
                e_form.save()
                ct_form.save()
                o_form.save()
                st_edu_form.save()
                messages.success(request, f'成功')
                return redirect('profile')
            '''
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        e_form = EduProfileUpdateForm(instance=request.user.profile)
        ct_form = CanTeachForm(instance=request.user.profile)
        o_form = OtherInfoForm(instance=request.user.profile)
        st_edu_form = studentEduStateForm(instance=request.user.profile)
        school_profile_form = schoolProfileForm(instance=request.user.profile)
    #if not request.user.is_authenticated:
        #return render(request, 'users/logout.html', {})
    
    return render(request, 'users/profile.html',{
        'UpTabletColor': UpTabletColor,
        'u_form' : u_form,
        'p_form' : p_form,
        'e_form' : e_form,
        'ct_form' : ct_form,
        'o_form' : o_form,
        'st_edu_form' : st_edu_form,
        'school_profile_form' : school_profile_form,
        })

@login_required
def schedule(request):
    if not request.user.is_authenticated:
        return render(request, 'users/logout.html', {})
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    return render(request, 'users/schedule.html', {
		'UpTabletColor': UpTabletColor,
		})

def exam(request):
    if not request.user.is_student:
        return render(request, 'users/logout.html', {})
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    return render(request, 'users/student/price_class_info.html', {
		'UpTabletColor': UpTabletColor,
		})
@login_required
def infoClass(request):
    if not (request.user.is_school or request.user.is_staff): #super admin
        return render(request, 'users/logout.html', {})
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    return render(request, 'users/school/price_class_info.html', {
		'UpTabletColor': UpTabletColor,
		})
        
# Job Pool response can be access by Tutor and SuperAdmin
@login_required
def JobPool(request):
    if not (request.user.is_tutor or request.user.is_staff):
        return render(request, 'users/logout.html', {})

    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    queryset = PostClass.objects.filter(status=1).order_by('-date_posted')
    
    return render( request, 'users/tutor/job_pool.html', 
    {'UpTabletColor': UpTabletColor, 'postclass':queryset})

#TODO Pagenation https://docs.djangoproject.com/en/3.2/topics/pagination/
@login_required
def Job(request, pk):
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    existClassObj = get_object_or_404(PostClass , id = pk)
    return render(request, 'users/tutor/Job.html' , {'UpTabletColor': UpTabletColor, 'postclass': existClassObj} )
##############################################

#TODO Pagenation https://docs.djangoproject.com/en/3.2/topics/pagination/
@login_required
def ClassListView(request):
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-default border-bottom'

    #Post class share response both Tutor and School
    # Situation 1 : Tutor filter with the PostClass [teacher] matches
    # Situation 2 : School filter with the PostClass [author] matches
    # Situation 3 : Superadmin return all in PostClass
    # if not request.user.is_authenticated:
    #     return redirect('login')

    if request.user.is_tutor: #return tutor joined object
        userObj = get_object_or_404(TutorUser, user = request.user)
        queryset = PostClass.objects.filter(teacher = userObj).order_by('-date_posted')
    elif request.user.is_school: #return school related object
        queryset = PostClass.objects.filter(author = request.user).order_by('-date_posted')
    elif request.user.is_staff: #superadmin return all objects in postclass
        queryset = PostClass.objects.all()
    
    return render( request, 'users/school/class.html', 
    {'UpTabletColor': UpTabletColor, 'postclass':queryset})

@login_required
def ClassDetailView(request, pk):
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-default border-bottom'
    existClassObj = get_object_or_404(PostClass , id = pk)
    return render(request, 'users/school/postclass_detail.html' , {'UpTabletColor': UpTabletColor, 'postclass': existClassObj} )

@login_required
def ClassUpdateView(request, pk):
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-default border-bottom'

    # TODO try catch handling
    existClassObj =  get_object_or_404(PostClass, id=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # Update existing instance form
        form = classUpdateForm(request.POST, instance=existClassObj)
        if form.is_valid():
            form.save()
            return redirect('Iclass')
    else:
        form = classUpdateForm(instance=existClassObj)
    return render(request, 'users/school/post_form.html', {'UpTabletColor' : UpTabletColor, 'form': form})

@login_required
def ClassCreateView(request):
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-default border-bottom'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = classCreateForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.updated_by = request.user
            form.save()
            return redirect('Iclass')
    else:
        form = classCreateForm()
    return render(request, 'users/school/post_form.html', {'UpTabletColor' : UpTabletColor, 'form': form})

@login_required
def ClassDelete(request, pk):
    instance = PostClass.objects.get(id = pk)
    if request.user == instance.author:
        instance.delete()
    return redirect('Iclass')

