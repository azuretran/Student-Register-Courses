from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.utils.dateparse import datetime_re
from django.utils.timezone import get_fixed_timezone
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime
from datetime import timedelta

from pytz import utc

from .encryption_util import *

import pendulum
from .models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel,  FeedBackStaffs_GV,Staffs_GV_HP,Time_subject,THUCHANH,Nhom_TH,Details_Subjects,PHONGHOC,PHIEUDK_HP,Time_register,result_tkb_dk


def staff_gv_home(request):
    phonghoc_count = PHONGHOC.objects.all().count()
    SessionYearModel_count = SessionYearModel.objects.all().count()
    Subjects_count = Subjects.objects.all().count()
    Nhom_TH_count = Nhom_TH.objects.all().count()

    context = {
        "phonghoc_count": phonghoc_count,
        "SessionYearModel_count":SessionYearModel_count,
        "Subjects_count":Subjects_count,
        "Nhom_TH_count":Nhom_TH_count
    }

    return render(request, "staff_gv_template/staff_home_template.html",context)
def staff_gv_feedback(request):
    staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs_GV.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_gv_template/staff_feedback_template.html", context)


def staff_gv_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_gv_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs_GV(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_gv_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_gv_feedback')
def staff_gv_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs_GV_HP.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_gv_template/staff_profile.html', context)





def staff_gv_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_gv_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs_GV_HP.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Cập Nhật Thành Công")
            return redirect('staff_profile')
        except:
            messages.error(request, "Cập Nhật Thất Bại")
            return redirect('staff_gv_profile')
# session
def manage_session_gv(request):
    session_years = SessionYearModel.objects.values('id','session_start_year','session_end_year')
    l=[]
    for i in session_years:
        i['encrypt_key'] = encrypt(i['id'])
        i['id'] = i['id']
        l.append(i)

    context = {
        "session_years": l
    }
    return render(request, "staff_gv_template/manage_session_template.html", context)


def add_session_gv(request):
    return render(request, "staff_gv_template/add_session_template.html")

def parse_datetime(value):
    """Parse a string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raise ValueError if the input is well formatted but not a valid datetime.
    Return None if the input isn't well formatted.
    """
    match = datetime_re.match(value)
    if match:
        kw = match.groupdict()
        kw['microsecond'] = kw['microsecond'] and kw['microsecond'].ljust(6, '0')
        tzinfo = kw.pop('tzinfo')
        if tzinfo == 'Z':
            tzinfo = utc
        elif tzinfo is not None:
            offset_mins = int(tzinfo[-2:]) if len(tzinfo) > 3 else 0
            offset = 60 * int(tzinfo[1:3]) + offset_mins
            if tzinfo[0] == '-':
                offset = -offset
            tzinfo = get_fixed_timezone(offset)
        kw = {k: int(v) for k, v in kw.items() if v is not None}
        kw['tzinfo'] = tzinfo
        return datetime.datetime(**kw)

def add_session_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Thêm Học Kì Thành Công!")
            return redirect("add_session_gv")
        except:
            messages.error(request, "Thêm Học Kì Thất Bại")
            return redirect("add_session_gv")


def edit_session_gv(request, session_id):
    session_id=decrypt(session_id)
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "staff_gv_template/edit_session_template.html", context)


def edit_session_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session_gv')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Cập Nhật Học Kì Thành Công.")
            return redirect('/edit_session_gv/'+session_id)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_session_gv/'+session_id)


def delete_session_gv(request, session_id):
    session_id = decrypt(session_id)
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Xoá Học Kì Thành Công!.")
        return redirect('manage_session_gv')
    except:
        messages.error(request, "Xoá Học Kì Thất Bại.")
        return redirect('manage_session_gv')
#time study subject
def manage_time_study(request):
    session_years = Time_subject.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "staff_gv_template/manage_time_study_template.html", context)

def add_time_study_gv(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "staff_gv_template/add_time_study_template.html",context)
def add_time_study_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')
        course_id = request.POST.get('course')
        course =SessionYearModel.objects.get(id=course_id)
        try:
            tghoc = Time_subject(start_day=start_day, end_day=end_day,Mahocki=course)
            tghoc.save()
            messages.success(request, "Thêm TG Học Thành Công!")
            return redirect("add_time_study_gv")
        except:
            messages.error(request, "Thêm TG Học Thất Bại")
            return redirect("add_time_study_gv")
def edit_time_study(request, Study_id):
    tghoc = Time_subject.objects.get(ID_time=Study_id)
    session_years = SessionYearModel.objects.all()
    context = {
        "tghoc": tghoc,
        "session_years": session_years,
        "ID_time":Study_id,

    }
    return render(request, 'staff_gv_template/edit_time_study_template.html', context)


def edit_time_study_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        Study_id=request.POST.get('Study_id')
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')
        course_id = request.POST.get('course')
        course = SessionYearModel.objects.get(id=course_id)
        try:
            tghoc = Time_subject.objects.get(ID_time=Study_id)

            tghoc.start_day = start_day
            tghoc.end_day = end_day
            tghoc.Mahocki = course
            tghoc.save()
            messages.success(request, "Cập Nhật Thành Công.")
            return redirect('/edit_time_study/' + Study_id)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_time_study/' + Study_id)


def delete_time_study(request, Study_id):
    tghoc = Time_subject.objects.get(ID_time=Study_id)
    try:
        tghoc.delete()
        messages.success(request, "Xoá Tg Học  Thành Công.")
        return redirect('manage_time_study')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_time_study')
#thuc hanh
def add_thuchanh_gv(request):

    return render(request, 'staff_gv_template/add_thuchanh_template.html')
def manage_thuchanh_gv(request):
    thuchanh = THUCHANH.objects.all()
    context = {
        "thuchanh": thuchanh
    }
    return render(request, "staff_gv_template/manage_thuchanh_template.html", context)

def add_thuchanh_gv_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        MATH = request.POST.get('MATH')
        soTietTH = request.POST.get('soTietTH')

        try:
            thuchanh = THUCHANH(MATH=MATH, soTietTH=soTietTH)
            thuchanh.save()
            messages.success(request, "Thêm  Thành Công!")
            return redirect("add_thuchanh_gv")
        except:
            messages.error(request, "Thêm  Thất Bại")
            return redirect("add_thuchanh_gv")
def edit_thuchanh_study(request, maTH):
    thuchanh = THUCHANH.objects.get(MATH=maTH)
    context = {
        "thuchanh": thuchanh,

    }
    return render(request, 'staff_gv_template/edit_thuchanh_template.html', context)


def edit_thuchanh_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:

        MATH = request.POST.get('MATH')
        soTietTH = request.POST.get('soTietTH')
        try:
            thuchanh = THUCHANH.objects.get(MATH=MATH)
            thuchanh.soTietTH = soTietTH
            thuchanh.save()
            messages.success(request, "Cập Nhật Thành Công.")
            return redirect('/edit_thuchanh_study/' + MATH)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_thuchanh_study/' + MATH)


def delete_thuchanh_study(request, maTH):
    tghoc = THUCHANH.objects.get(MATH=maTH)
    try:
        tghoc.delete()
        messages.success(request, "Xoá Thực Hành Thành Công.")
        return redirect('manage_thuchanh_gv')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_thuchanh_gv')
#nhom thuc hanh
def add_nhom_TH(request):
    tghoc = THUCHANH.objects.all()
    session=SessionYearModel.objects.all()
    context = {
        "tghoc": tghoc,
        "session":session,
    }
    return render(request, 'staff_gv_template/add_nhomTH_template.html',context)
def manage_nhomTH_gv(request):
    nhomth = Nhom_TH.objects.all()
    context = {
        "nhomth": nhomth,
    }
    return render(request, "staff_gv_template/manage_nhomTH_template.html", context)

def add_nhomTH_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:

        math_id = request.POST.get('course')
        MATH = THUCHANH.objects.get(MATH=math_id)
        startday_TH = request.POST.get('startday_TH')
        end_day = request.POST.get('end_day')
        name_nhom = request.POST.get('name_nhom')
        buoihoc = request.POST.get('buoihoc')


        try:
            thuchanh = Nhom_TH(MATH=MATH, startday_TH=startday_TH,endday_TH=end_day,name_nhom=name_nhom,buoihoc=buoihoc)
            thuchanh.save()
            messages.success(request, "Thêm  Thành Công!")
            return redirect("add_nhom_TH")
        except:
            messages.error(request, "Thêm  Thất Bại")
            return redirect("add_nhom_TH")
def edit_nhomTH_study(request, MATH):
    tghoc = Nhom_TH.objects.get(id=MATH)
    session=SessionYearModel.objects.all()
    tghoc1 = THUCHANH.objects.all()
    context = {
        "tghoc": tghoc,
        "session":session,
        "tghoc1":tghoc1,

    }
    return render(request, 'staff_gv_template/edit_nhomTH_template.html', context)


def edit_nhomTH_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        session_id = request.POST.get('MATH')
        math_id = request.POST.get('course')
        MATH = THUCHANH.objects.get(MATH=math_id)
        MATH_1 = SessionYearModel.objects.get(id=math_id_1)
        startday_TH = request.POST.get('startday_TH')
        endday_TH = request.POST.get('endday_TH')
        name_nhom = request.POST.get('name_nhom')
        try:
            thuchanh = Nhom_TH.objects.get(id=session_id)
            thuchanh.MATH =MATH
            thuchanh.startday_TH =startday_TH
            thuchanh. endday_TH =endday_TH
            thuchanh.name_nhom =name_nhom
            thuchanh.save()
            messages.success(request, "Cập Nhật Thành Công.")
            return redirect('/edit_nhomTH_study/' + session_id)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_nhomTH_study/' + session_id)


def delete_nhomTH_study(request, id):
    tghoc = Nhom_TH.objects.get(id=id)
    try:
        tghoc.delete()
        messages.success(request, "Xoá  Thành Công.")
        return redirect('manage_nhomTH_gv')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_nhomTH_gv')
@csrf_exempt
def check_tkb_exist(request):
    th_id = request.POST.get('th_id')
    tghoc = Nhom_TH.objects.filter(id=th_id).exists()
    if tghoc:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def show_tkb_nhomTH_study(request):
    th_id = request.POST.get('th_id')
    tghoc = Nhom_TH.objects.get(id=th_id)
    start_day=tghoc.startday_TH
    end_day=tghoc.endday_TH
    buoihoc = tghoc.buoihoc
    if buoihoc == 5 :
        end_day = end_day + timedelta(hours=buoihoc)
    if buoihoc == 10 :
        start_day = start_day + timedelta(hours=buoihoc)
        end_day = end_day + timedelta(hours=buoihoc)
    start = pendulum.datetime(start_day.year,start_day.month,start_day.day)
    end = pendulum.datetime(end_day.year,end_day.month,end_day.day)
    period = pendulum.period(start, end)
    for dt in period.range('weeks'):

            result=result_tkb_dk(Nhom_TH=tghoc,startday_TH=dt,endday_TH=dt)
            result.save()

    return HttpResponse("True")

#manage subject
def add_subject_gv(request):

    staffs = CustomUser.objects.filter(user_type='2')
    time_subject=Time_subject.objects.get.all()
    thuchanhs=THUCHANH.objects.get.all()
    context = {
        "time_subject":time_subject,
        "staffs": staffs,
        "thuchanhs":thuchanhs,
    }
    return render(request, 'hod_template/add_subject_template.html', context)

def manage_subject_gv(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'staff_gv_template/manage_subject_template.html', context)
def add_subject_gv(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    time_subjects = Time_subject.objects.all()
    thuchanhs = THUCHANH.objects.all()
    context = {
        "courses": courses,
        "staffs": staffs,
        "time_subjects":time_subjects,
        "thuchanhs":thuchanhs,
    }
    return render(request, 'staff_gv_template/add_subject_template.html', context)



def add_subject_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject_gv')
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        so_tc = request.POST.get('so_tc')
        tongsvdk = request.POST.get('tongsvdk')
        nienkhoa =request.POST.get('nienkhoa')
        Time_subject_id= request.POST.get('ID_time')
        time_subject=Time_subject.objects.get(ID_time=Time_subject_id)
        THUCHANH_id=request.POST.get('MATH')
        math=THUCHANH.objects.get(MATH=THUCHANH_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff,so_tc=so_tc,tongsvdk=tongsvdk,nienkhoa=nienkhoa,ID_time=time_subject,MATH= math)

            subject.save()
            messages.success(request, "Thêm Môn Học Thành Công!")
            return redirect('add_subject_gv')
        except:
            messages.error(request, "Thêm Môn Học Thất Bại!")
            return redirect('add_subject_gv')


def edit_subject_gv(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    time_subjects = Time_subject.objects.all()
    thuchanhs = THUCHANH.objects.all()
    context = {
        "courses": courses,
        "staffs": staffs,
        "time_subjects": time_subjects,
        "thuchanhs": thuchanhs,
        "subject":subject,
    }
    return render(request, 'staff_gv_template/edit_subject_template.html', context)


def edit_subject_save_gv(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')
        so_tc = request.POST.get('so_tc')
        tongsvdk = request.POST.get('tongsvdk')
        nienkhoa = request.POST.get('nienkhoa')
        Time_subject_id= request.POST.get('ID_time')
        THUCHANH_id = request.POST.get('MATH')
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            subject.so_tc = so_tc
            subject.tongsvdk = tongsvdk
            subject.nienkhoa = nienkhoa
            staff_1 = Time_subject.objects.get(ID_time=Time_subject_id)
            subject.ID_time = staff_1
            staff_2 = THUCHANH.objects.get(ID_time=THUCHANH_id)
            subject.MATH = staff_2

            subject.save()

            messages.success(request, "Cập Nhật Môn Học Thành Công.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject_gv", kwargs={"subject_id": subject_id}))

        except:
            messages.error(request, "Cập Nhật Môn Học Thất Bại.")
            return HttpResponseRedirect(reverse("edit_subject_gv", kwargs={"subject_id": subject_id}))
            # return redirect('/edit_subject/'+subject_id)


def delete_subject_gv(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Xoá Môn Học Thành Công.")
        return redirect('manage_subject_gv')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_subject_gv')
#gia mon hoc
def manage_subject_price_gv(request):
    price_subject = Details_Subjects.objects.all()
    context = {
        "price_subject": price_subject
    }
    return render(request, "staff_gv_template/manage_price_subject_template.html", context)


def add_price_subject_gv(request):
    subject = Subjects.objects.all()
    context = {
        "subject": subject
    }
    return render(request, "staff_gv_template/add_price_subject_template.html",context)


def add_price_subject_gv_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_price_subject_gv')
    else:
        course_id = request.POST.get('MAMH')
        course = Subjects.objects.get(id=course_id)
        GiaTC = request.POST.get('GiaTC')
        try:
            price_subject = Details_Subjects(MAMH=course, GiaTC=GiaTC)
            price_subject.save()
            messages.success(request, "Thêm Giá Thành Công!")
            return redirect("add_price_subject_gv")
        except:
            messages.error(request, "Thêm Giá Thất Bại")
            return redirect("add_price_subject_gv")


def edit_subject_price_gv(request, subject_id):
    giatc = Details_Subjects.objects.get(MAMH=subject_id)
    subject = Subjects.objects.all()
    context = {
        "giatc": giatc,
        "subject": subject
    }
    return render(request, "staff_gv_template/edit_price_subject_template.html", context)


def edit_subject_price_gv_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_subject_price_gv')
    else:
        iatc=request.POST.get('GiaTC')
        subject_id=request.POST.get('subject_id')
        try:
            giatc = Details_Subjects.objects.get(MAMH=subject_id)
            giatc.GiaTC = iatc

            giatc.save()

            messages.success(request, "Cập Nhật Giá Thành Công.")
            return redirect('/edit_subject_price_gv/'+subject_id)
        except:
            messages.error(request, "Cập Nhật Giá Thất Bại.")
            return redirect('/edit_subject_price_gv/'+subject_id)


def delete_subject_price_gv(request, subject_id):
    session = Details_Subjects.objects.get(MAMH=subject_id)
    try:
        session.delete()
        messages.success(request, "Xoá Thành Công.")
        return redirect('manage_subject_price_gv')
    except:
        messages.error(request, "Xoá Thất Bại.")
        return redirect('manage_subject_price_gv')
#manage room service
def manage_room_gv(request):
    rooms = PHONGHOC.objects.all()
    context = {
        "rooms": rooms
    }
    return render(request, "staff_gv_template/manage_room_template.html", context)

def manage_room_gv_search(request):
    room1 = request.POST.get("MAPHONG")
    rooms = PHONGHOC.objects.filter(MAPHONG=room1)
    context = {
        "rooms": rooms,
        "room1": room1
    }
    return render(request, "staff_gv_template/search_template.html",context)

def add_room_gv(request):
    MAMH=request.POST.get('MAMH')
    subject = Subjects.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs_GV_HP.objects.get(admin=user)
    nhoms=Nhom_TH.objects.all()
    context = {
        "subject": subject,
        "staff": staff,
        "user": user,
        "nhoms":nhoms,

    }
    return render(request, "staff_gv_template/add_room_template.html",context)


def add_room_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_room_gv')
    else:
        MAPHONG = request.POST.get('MAPHONG')
        Siso_phong = request.POST.get('Siso_phong')
        course_id = request.POST.get('MAMH')
        course = Subjects.objects.get(id=course_id)
        gv_id = request.POST.get('MAGVCAPPHONG')
        gv = Staffs_GV_HP.objects.get(id=gv_id)
        MA_TH=request.POST.get('MA_TH')
        try:
            room = PHONGHOC(MAPHONG=MAPHONG,Siso_phong=Siso_phong,MAMH=course,
                            MAGVCAPPHONG=gv,MA_TH=MA_TH)
            room.save()
            messages.success(request, "Thêm Phòng Học Thành Công!")
            return redirect("add_room_gv")
        except:
            messages.error(request, "Thêm Phòng Học Thất Bại")
            return redirect("add_room_gv")


def edit_room_gv(request, room_id):
    rooms=PHONGHOC.objects.get(MAPHONG=room_id)
    subject = Subjects.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs_GV_HP.objects.get(admin=user)
    nhoms = Nhom_TH.objects.all()
    context = {
        "subject": subject,
        "staff": staff,
        "user": user,
        "rooms":rooms,
        "nhoms":nhoms,
    }

    return render(request, "staff_gv_template/edit_room_template.html", context)


def edit_room_gv_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_room_gv')
    else:
        room_id = request.POST.get('room_id')
        Siso_phong = request.POST.get('Siso_phong')
        MAMH = request.POST.get('MAMH')
        course = Subjects.objects.get(id=MAMH)

        gv_id = request.POST.get('MAGVCAPPHONG')
        gv = Staffs_GV_HP.objects.get(id=gv_id)
        MA_TH = request.POST.get('MA_TH')
        try:
            room = PHONGHOC.objects.get(MAPHONG=room_id)
            room.Siso_phong = Siso_phong
            room.MAMH = course
            room.MAGVCAPPHONG = gv
            room.MA_TH = MA_TH

            room.save()

            messages.success(request, "Cập Nhật Thông Tin Phòng Thành Công.")
            return redirect('/edit_room_gv/'+room_id)
        except:
            messages.error(request, "Cập Nhật Thông Tin Phòng Thất Bại.")
            return redirect('/edit_room_gv/'+room_id)


def delete_room_gv(request, room_id):
    session = PHONGHOC.objects.get(MAPHONG=room_id)
    try:
        session.delete()
        messages.success(request, "Xoá Thành Công.")
        return redirect('manage_room_gv')
    except:
        messages.error(request, "Xoá Thất Bại.")
        return redirect('manage_room_gv')


def manage_sum_teach_teamplate(request):

    subject = Subjects.objects.all()
    context={
        "subject":subject
    }
    return render(request, "staff_gv_template/manage_sum_teach_teamplate.html",context)

@csrf_exempt
def check_room_exist(request):
    room = request.POST.get("room")
    room_obj = PHONGHOC.objects.filter(MAPHONG=room).exists()
    if room_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
@csrf_exempt
def check_thuchanh_exist(request):
    math = request.POST.get("math")
    math_obj = THUCHANH.objects.filter(MATH=math).exists()
    if math_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
@csrf_exempt
def check_nhom_name_exist(request):
    math = request.POST.get("math")
    thuchanh_model=THUCHANH.objects.get(MATH=math)
    nhom_name = request.POST.get("nhom_name")
    math_obj = Nhom_TH.objects.filter(name_nhom=nhom_name,MATH=thuchanh_model).exists()
    if math_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
@csrf_exempt
def check_room_exist_together(request):
    room = request.POST.get("room")
    room_obj = PHONGHOC.objects.filter(MAPHONG=room).exists()
    #buoihoc
    room = request.POST.get("room")
    room_obj = PHONGHOC.objects.filter(MAPHONG=room).exists()
    #thu
    room = request.POST.get("room")
    room_obj = PHONGHOC.objects.filter(MAPHONG=room).exists()
    #mamonhoc
    room = request.POST.get("room")
    room_obj = PHONGHOC.objects.filter(MAPHONG=room).exists()
    if room_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
@csrf_exempt
def check_session_day(request):
    mahocki = request.POST.get("mahocki")
    room_obj=SessionYearModel.objects.get(id=mahocki)
    if room_obj:
        return room_obj.session_start_year
    else:
        return HttpResponse(False)

def staff_feedback_gv(request):
    staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs_GV.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_gv_template/staff_feedback_template.html", context)




def staff_feedback_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs_GV(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Gửi Thành Công! Xin Cảm Ơn.")
            return redirect('staff_feedback_gv')
        except:
            messages.error(request, "Gửi Thất Bại.")
            return redirect('staff_feedback_gv')
def manage_subject_teach_gv_hp(request):
    phieudk=PHIEUDK_HP.objects.all()
    context = {
        "phieudk": phieudk
    }
    return render(request, "staff_gv_template/manage_confirm_register_template.html",context)

def manage_time_register_template(request):
    times=Time_register.objects.all()
    context = {
        "times": times
    }
    return render(request, "staff_gv_template/manage_time_register_template.html",context)
#time register
def add_time_register(request):
    times = Students.objects.all()
    context = {
        "times": times
    }
    return render(request, "staff_gv_template/add_time_register_template.html",context)


def add_time_register_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_time_register')
    else:
        start_day_register = request.POST.get('start_day_register')
        enday_register = request.POST.get('enday_register')
        nienkhoa = request.POST.get('nienkhoa')
        user = CustomUser.objects.get(id=request.user.id)
        staff_model = Staffs_GV_HP.objects.get(admin=user)
        try:
            price_subject = Time_register(staff_id=staff_model.admin, start_day_register=start_day_register,enday_register=enday_register,nienkhoa=nienkhoa)
            price_subject.save()
            messages.success(request, "Thêm  Thành Công!")
            return redirect("add_time_register")
        except:
            messages.error(request, "Thêm  Thất Bại")
            return redirect("add_time_register")


def edit_time_register(request, time_id):
    giatc = Time_register.objects.get(id=time_id)
    times = Students.objects.all()
    context = {
        "giatc": giatc,
        "times":times,

    }
    return render(request, "staff_gv_template/edit_time_register_template.html", context)


def edit_time_register_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_time_register_template')
    else:
        time_id = request.POST.get('time_id')
        start_day_register = request.POST.get('start_day_register')
        enday_register = request.POST.get('enday_register')
        nienkhoa = request.POST.get('nienkhoa')
        user = CustomUser.objects.get(id=request.user.id)
        staff_model = Staffs_GV_HP.objects.get(admin=user)
        try:
            giatc = Time_register.objects.get(id=time_id)
            giatc.staff_id = staff_model.admin
            giatc.start_day_register = start_day_register
            giatc.enday_register = enday_register
            giatc.nienkhoa = nienkhoa
            giatc.save()
            messages.success(request, "Cập Nhật Thời Gian Đăng Kí Thành Công.")
            return redirect('/edit_time_register/'+time_id)
        except:
            messages.error(request, "Cập Nhật  Thời Gian Đăng Kí Thất Bại.")
            return redirect('/edit_time_register/'+time_id)


def delete_time_register(request, time_id):
    session = Time_register.objects.get(id=time_id)
    try:
        session.delete()
        messages.success(request, "Xoá Thành Công.")
        return redirect('manage_time_register_template')
    except:
        messages.error(request, "Xoá Thất Bại.")
        return redirect('manage_time_register_template')