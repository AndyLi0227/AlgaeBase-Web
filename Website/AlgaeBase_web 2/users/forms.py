from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.views.generic.edit import FormMixin
from .models import User, StudentUser, TutorUser, SchoolUser, Profile, PostClass #, EduProfile
from crispy_forms.helper import FormHelper

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    whatsapp_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = StudentUser.objects.create(user=user)
        user.phone_number=self.cleaned_data.get('phone_number')
        user.whatsapp_number=self.cleaned_data.get('whatsapp_number')
        user.email=self.cleaned_data.get('email')
        user.save()
        #student.save()
        return user

class TutorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    whatsapp_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        tutor = TutorUser.objects.create(user=user)
        user.phone_number=self.cleaned_data.get('phone_number')
        user.whatsapp_number=self.cleaned_data.get('whatsapp_number')
        user.email=self.cleaned_data.get('email')
        user.save()
        #tutor.save()
        return user
        
class SchoolSignUpForm(UserCreationForm):
    #first_name = forms.CharField(required=True)
    #last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    whatsapp_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_school = True
        user.is_staff = True
        #user.first_name = self.cleaned_data.get('first_name')
        #user.last_name = self.cleaned_data.get('last_name')
        user.save()
        school = SchoolUser.objects.create(user=user)
        user.phone_number=self.cleaned_data.get('phone_number')
        user.whatsapp_number=self.cleaned_data.get('whatsapp_number')
        user.email=self.cleaned_data.get('email')
        user.save()
        #school.save()
        return user


class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField()
    whatsapp_number = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['phone_number','whatsapp_number','email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image',
            'gender_field',
            'ch_last_name',
            'ch_first_name',
            'date_of_birth',
            ]

class EduProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'edu_state',
            'edu_school',
            'edu_major',
            'provement',
            ]
class CanTeachForm(forms.ModelForm):
    可補習地區 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=Profile.profile_location)
    class Meta:
        model = Profile
        fields = [
            #'min_pay',
            '可補習地區', 
            ]

class OtherInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'living_place',
            'high_school', 
            'now_job',
            'now_job_place',
            #'exam_results',
            'other_skills_provement',
            ]

class studentEduStateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'student_edu_state',
            ]

class schoolProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image',
            'school_address',
            ]

class classCreateForm(forms.ModelForm):
    class Meta:
        model = PostClass
        fields = [
            'course_option', 
            'classPlace', 
            'classDates', 
            'classStartTime',
            'classEndTime', 
            'content',
            ]

class classUpdateForm(forms.ModelForm):
    class Meta:
        model = PostClass
        fields = [
            'course_option', 
            'classPlace',
            'classDates',
            'classStartTime',
            'classEndTime',
            'content',
            ]
            
#reference:
'''
class PensonalInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            '',
            '', 
            '', 
            '',
            '',
            ]
'''