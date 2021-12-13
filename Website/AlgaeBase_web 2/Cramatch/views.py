from datetime import datetime
import re
from django.http.response import HttpResponse
from django.shortcuts import render
#from django.http import HttpResponse
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from users import models
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404
from users.models import PostClass, TutorUser, TimeTableItem
from django.shortcuts import redirect

from django.core.mail import message, send_mail
from django.conf import settings
#python lib
from datetime import datetime

def index(request):
	return render(request, 'cramatch/index.html', {'title': 'index'})

def loginIndex(request):
	return render(request, 'login_index.html', {'title': 'login System'})

def bypass(request):
	UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
	if request.user.is_authenticated:
		if request.user.is_tutor:
			return render(request, 'dashboard.html', {'UpTabletColor': UpTabletColor,})
		elif request.user.is_student:
			return render(request, 'stud_dash.html', {'UpTabletColor': 'navbar navbar-top navbar-expand navbar-dark bg-danger border-bottom',})
		else:
			return render(request, 'school_dash.html', {'UpTabletColor': 'navbar navbar-top navbar-expand navbar-dark bg-green border-bottom',})
	return render(request, 'users/logout.html', {})

def dashboardView(request):
    if not (request.user.is_tutor or request.user.is_staff):
        return render(request, 'users/logout.html', {})
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    return render(request, 'dashboard.html', {
		'UpTabletColor': UpTabletColor,
		})

def stud_dash(request):
    if not request.user.is_student:
        return render(request, 'users/logout.html', {})
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    return render(request, 'stud_dash.html', {
		'UpTabletColor': UpTabletColor,
		})

def school_dash(request):
    if not (request.user.is_school or request.user.is_staff):
        return render(request, 'users/logout.html', {})
    UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-primary border-bottom'
    return render(request, 'school_dash.html', {
		'UpTabletColor': UpTabletColor,
		})

#tutor action
def applyJob(request, pk):
	postclass_obj = get_object_or_404(PostClass,pk=pk)
	#TODO postclass 404
	if request.user.is_tutor:
		#validation
		istimeoverlap = True
		#step1 get the dates will be assigned
		target_dates = postclass_obj.classDates
		target_starttime = postclass_obj.classStartTime
		target_endtime = postclass_obj.classEndTime
		#step2 change to array format of dates string
		target_dates_arr = [x.strip() for x in target_dates.split(',')]
		print("target_dates_arr: ")
		print(target_dates_arr)
		#step3 fetch TimeTableItem with user and dates
		existing_timetableItems = TimeTableItem.objects.filter(user=request.user, item_date__in = target_dates_arr)
		#step4 loop dates objects for checking
		print("existing_timetableItems: ")
		print(existing_timetableItems)
		if existing_timetableItems:
			for existing_timetableItem in existing_timetableItems:
				existing_item_starttime = existing_timetableItem.start_time
				existing_item_endtime = existing_timetableItem.end_time
				if not isTimeRangeExist(target_starttime, target_endtime, existing_item_starttime, existing_item_endtime):
					istimeoverlap = False
					UpTabletColor = 'navbar navbar-top navbar-expand navbar-dark bg-default border-bottom'
					alerttype = 'alert-danger'
					overlap_item_name = existing_timetableItem.item_name
					alertmessage = 'timeslot overlap registered item : '+overlap_item_name
					return render( request, 'users/tutor/Job.html', {'UpTabletColor': UpTabletColor, 'postclass':postclass_obj, 'alerttype': alerttype, 'message': alertmessage})
		else:
			print("existing_timetableItems none")
			istimeoverlap = False

		#TODO handle istimeoverlap exception
		print("istimeoverlap :")
		print(istimeoverlap)
		if not istimeoverlap:
			#Update postclass
			postclass_obj.teacher = get_object_or_404(TutorUser,user=request.user)
			postclass_obj.updated_by = request.user.username
			postclass_obj.status = 4
			postclass_obj.save(update_fields=['teacher','status','updated_at','updated_by'])
			#Update timetableItem
			for target_date in target_dates_arr:
				new_item = TimeTableItem(\
					user=request.user, \
					item_date=target_date, \
					start_time=target_starttime,\
					end_time=target_endtime,\
					item_name=postclass_obj.course_option
					)
				new_item.save()

	return redirect('/JobPool/')

def isTimeRangeExist(n_start_time, n_end_time, start_time, end_time):
	#case 1 : new starttime within existing range
	#case 2 : new endtime within existing range
	#case 3 : existing starttime within new time range
	#case 4 : existing endtime within new time range
	#TODO consider new start time is overlap existing endtime at 1500?? 1459?? how to handle
	if  (n_start_time >= start_time and n_start_time <= end_time) or \
		(n_end_time >= start_time and n_end_time <= end_time) or \
		(start_time >= n_start_time and start_time <= n_end_time) or \
		(end_time >= n_start_time and end_time <= n_end_time):
		return True
	return False

#author action
def applyJobApprove(request, pk):
	postclass_obj = get_object_or_404(PostClass,pk=pk)
	if postclass_obj.author == request.user:
		postclass_obj.updated_by = request.user.username
		postclass_obj.status = 4
		postclass_obj.save(update_fields=['status','updated_at','updated_by'])
	return redirect('/Iclass')

def applyJobOpen(request, pk):
	postclass_obj = get_object_or_404(PostClass,pk=pk)
	if postclass_obj.author == request.user:
		postclass_obj.updated_by = request.user.username
		postclass_obj.status = 1
		postclass_obj.save(update_fields=['status','updated_at','updated_by'])
	return redirect('/Iclass')

def applyJobClose(request, pk):
	postclass_obj = get_object_or_404(PostClass,pk=pk)
	if postclass_obj.author == request.user:
		postclass_obj.updated_by = request.user.username
		postclass_obj.status = 2
		postclass_obj.save(update_fields=['status','updated_at','updated_by'])
	return redirect('/Iclass')