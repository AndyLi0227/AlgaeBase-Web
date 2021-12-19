from typing import DefaultDict, Text
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.fields.related import ForeignKey
from django.db.models.lookups import EndsWith
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from datetime import datetime, date, time

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()

class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    #phone_number = models.CharField(max_length=20)
    #whatsapp_number = models.CharField(max_length=20)
    #email = models.EmailField()

class TutorUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    #phone_number = models.CharField(max_length=20)
    #whatsapp_number = models.CharField(max_length=20)
    #email = models.EmailField()

class SchoolUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    #phone_number = models.CharField(max_length=20)
    #whatsapp_number = models.CharField(max_length=20)
    #email = models.EmailField()

class Profile(models.Model):
    profile_gender=(
        ('Undefine', '不透露'),('Male', '男性'),('Female', '女性')
    )
    profile_edu=(
        ('secondary','中學文憑畢業'),('hd', '⾼級文憑'),('asso', '副學⼠'),('degree', '學⼠'),('master', '碩⼠'),('phd', '博⼠'),
    )
    profile_location=(
            (11,'中西區'),
            (12,'東區'),
            (13,'南區'),
            (14,'灣仔區'),
            (21,'九龍城區'),
            (22,'觀塘區'),
            (23,'深水埗區'),
            (24,'黃大仙區'),
            (25,'油尖旺區'),
            (31,'離島區'),
            (32,'葵青區'),
            (33,'北區'),
            (34,'西貢區'),
            (35,'沙田區'),
            (36,'大埔區'),
            (37,'荃灣區'),
            (38,'屯門區'),
            (39,'元朗區'),
        )
    student_edu_state=[
        ('幼稚園', (
            ('一年班', '一年班'),
            ('二年班', '二年班'),
            ('三年班', '三年班'),
        )),
        ('小學', (
            ('小一', '小一'),
            ('小二', '小二'),
            ('小三', '小三'),
            ('小四', '小四'),
            ('小五', '小五'),
            ('小六', '小六'),
        )),
        ('中學', (
            ('中一', '中一'),
            ('中二', '中二'),
            ('中三', '中三'),
            ('中四', '中四'),
            ('中五', '中五'),
            ('中六', '中六'),
            ('自修生', '自修生'),
        )),
        ('其他', (
            ('基礎文憑', '基礎文憑'),
            ('高級文憑', '高級文憑'),
            ('副學士', '副學士'),
            ('學士', '學士'),
            ('成人補習', '成人補習'),
        )),
    ]
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField('Icon', default='default.jpg', upload_to='profile_pics')
    gender_field = models.CharField('性別', max_length=50, choices = profile_gender)
    ch_last_name = models.CharField('姓',max_length=100)
    ch_first_name = models.CharField('名',max_length=100)
    date_of_birth = models.DateField('生日', default=date.today().strftime('%Y-%m-%d')) #未計
    ###edu###
    edu_state = models.CharField('教育程度', max_length=50, choices = profile_edu)
    edu_school = models.CharField('就讀院校名稱', max_length=100, default="請填全寫")
    edu_major = models.CharField('主修', max_length=50, default="可以逗號填埋副修")
    provement = models.ImageField(upload_to='provement_pics')
    ###teach###
    可補習地區 = models.CharField(max_length=100)
    #min_pay = models.DecimalField('最低收費時薪 $',max_digits=5,decimal_places=0, null=True)
    ##other##
    living_place = models.CharField('居住地區', max_length=100, blank=True, default="地區 大廈名字即可")
    high_school = models.CharField('所讀中學', max_length=100, blank=True, default="中學校名")
    now_job = models.CharField('工作種類', max_length=100, blank=True, default="工作類別即可")
    now_job_place = models.CharField('工作地點', max_length=100, blank=True, default="工作區域即可")
    other_skills_provement = models.FileField('其他資歷/技能證書(如有) 例如：IELTS 7.5, TOEFL 95, 法⽂文C2等', max_length=1000, blank=True, default="全部證明壓縮為一即可")
    ##student##
    ##student_edu ######
    student_edu_state = models.CharField('學生年級', max_length=50,  null=True, choices = student_edu_state)
    student_school = models.CharField('就讀院校全稱', max_length=100, default="請填全寫")

    ##school ##
    ##school info##
    school_address = models.CharField('學校地址', max_length=100, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class PostClass(models.Model):
    _12course_list=(
        ('3d', '3D打印'),('robot', '機械人'),('hand', '機械臂'),('ecar', '電動車'),
        ('energy', '再生能源'),('planting', '室內種植'),('programming', '學習編程'),('space', '太空知識'),
        ('fintech', '新科技金融'),('sci', '科學探究'),('maths', '數理學'),('logic', '邏輯思維')
    )
    course_option = models.CharField('12課STEM核心班', max_length=100, choices = _12course_list, null=True)
    classPlace = models.CharField('上課地點(班房)',max_length=100)
    classDates = models.CharField('上課日期', max_length=255, null=True)
    classStartTime = models.TimeField('上課時間 (時：分)', default=datetime.now().strftime("%H:%M"))
    classEndTime = models.TimeField('下課時間 (時：分)', default=datetime.now().strftime("%H:%M"))
    content = models.TextField('補充資料', blank=True, null=True)
    date_posted = models.DateTimeField(editable=False, default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #matching usage
    POST_STATUS = (
        (1,'STATUS_OPEN'),
        (2,'STATUS_CLOSE'),
        (3,'STATUS_WAITING_APPROVAL'),
        (4,'STATUS_OCCUPIED'),
    )
    status = models.IntegerField('Status',editable=False, default=2, choices=POST_STATUS)
    #may be change to ManyToManyField sample below
    #https://newbedev.com/trying-to-make-a-postgresql-field-with-a-list-of-foreign-keys-in-django
    teacher = models.ForeignKey(TutorUser, editable=False, null=True, blank=True, on_delete=models.SET_NULL)
    #system log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30, default=author)
    # def __str__(self):
    #     return self.title

    def get_absolute_url(self):
        return reverse('Iclass-detail', kwargs={'pk': self.pk})

class TimeTableItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    item_date = models.DateField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    