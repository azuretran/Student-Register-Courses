from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import CustomUser, Subjects, Students, FeedBackStudent,PHONGHOC,Nhom_TH,Details_Subjects,PHIEUDK_HP,Time_register,result_tkb_dk

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)
def student_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff_model = Students.objects.get(admin=user)
    subject_register_count = PHIEUDK_HP.objects.filter(MASV=staff_model.admin).count
    subjects_count = Subjects.objects.filter(nienkhoa=staff_model.nienkhoa).count
    context = {
        "subject_register_count": subject_register_count,
        "subjects_count":subjects_count
    }
    return render(request, "student_template/student_home_template.html",context)




def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)



def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
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

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_register_course(request):

   # subjects = Subjects.objects.all()

    phongs=PHONGHOC.objects.all()
    nhoms=Nhom_TH.objects.all()
    price_subjects=Details_Subjects.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    staff_model = Students.objects.get(admin=user)
    subjects = Subjects.objects.filter(nienkhoa=staff_model.nienkhoa)
    time = Time_register.objects.filter(nienkhoa=staff_model.nienkhoa)
    phieu_dk = PHIEUDK_HP.objects.filter(MASV=staff_model.admin)
    context = {
        "subjects":subjects,
        "phongs":phongs,
        "nhoms": nhoms,
        "price_subjects":price_subjects,
        "phieu_dk":phieu_dk,
        "time":time,
    }
    return  render(request,"student_template/student_register_course.html",context)

def student_view_timetable(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff_model = Students.objects.get(admin=user)
    dk_model = PHIEUDK_HP.objects.filter(MASV=staff_model.admin)
    tgth=Nhom_TH.objects.all()
    tkb=result_tkb_dk.objects.all()
    subject=Subjects.objects.all()
    context = {
    "tgth":tgth,
    "dk_model":dk_model,
        "tkb":tkb,
            "subject":subject,
    }
    return  render(request,"student_template/student_view_timetable.html",context)

def student_view_diploma(request):

    user = CustomUser.objects.get(id=request.user.id)
    staff_model = Students.objects.get(admin=user)
    dk_model = PHIEUDK_HP.objects.filter(MASV=staff_model.admin)
    subjects = Subjects.objects.all()
    context = {
        "dk_model": dk_model,
        "subjects":subjects,

    }
    return  render(request,"student_template/student_view_diploma.html",context)

@csrf_exempt
def student_register(request):
    room_id = request.POST.get('room_id')
    ma_mh = request.POST.get('ma_mh')
    subject_model=Subjects.objects.get(id=ma_mh)
    user = CustomUser.objects.get(id=request.user.id)
    staff_model = Students.objects.get(admin=user)
    phong_model=PHONGHOC.objects.get(MAPHONG=room_id,MAMH=subject_model)
    try:
        feedback = PHIEUDK_HP(MASV=staff_model.admin,MAPHONG=phong_model)
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")
def student_result_register(request):
    results = PHIEUDK_HP.objects.all()
    tghocs = PHIEUDK_HP.objects.all()
    context = {
        "results": results,
        "tghocs":tghocs,

    }
    return render(request, "student_template/student_result_register_template.html", context)
def delete_dk_hp_study(request, maTH):
    tghoc = PHIEUDK_HP.objects.get(id=maTH)
    try:
        tghoc.delete()
        messages.success(request, "Xoá  Thành Công.")
        return redirect('student_result_register')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('student_result_register')
@csrf_exempt
def check_subject_register_exist(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff_model = Students.objects.get(admin=user)
    room_id = request.POST.get("room_id")
    ma_mh = request.POST.get("ma_mh")
    mohoc_model=Subjects.objects.get(id=ma_mh)
    phonghoc_model=PHONGHOC.objects.get(MAPHONG=room_id,MAMH=mohoc_model)
    dk_model = PHIEUDK_HP.objects.filter(MASV=staff_model.admin,MAPHONG=phonghoc_model.MAPHONG).exists()

    if dk_model:
        return HttpResponse(True)
    else:
        return HttpResponse(False)