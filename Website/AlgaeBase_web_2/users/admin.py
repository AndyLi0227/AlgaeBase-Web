from django.contrib import admin
from .models import User, StudentUser, TutorUser, SchoolUser, AlgaeUser, PostClass, Profile, TimeTableItem#, EduProfile


admin.site.register(User)
admin.site.register(StudentUser)
admin.site.register(TutorUser)
admin.site.register(SchoolUser)
admin.site.register(AlgaeUser)
# Register your models here.
class PostClassAdmin(admin.ModelAdmin):
    list_display = ('author','teacher', 'date_posted', 'status', 
                     'created_at', 'updated_at')
admin.site.register(PostClass,PostClassAdmin)
admin.site.register(Profile)
admin.site.register(TimeTableItem)
#admin.site.register(EduProfile)
