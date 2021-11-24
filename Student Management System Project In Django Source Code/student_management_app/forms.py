from django import forms 
from django.forms import Form
import time
from .validators import *
class DateInput(forms.DateInput):
    input_type = "date"
def return_tudongMSV():
    prefix = "svcntt"
    timestamp = str(int(time.time()) % 1624)
    default_value = prefix + timestamp
    return default_value


def return_tudongEmailSV():
    pre = "@student.ptithcm.edu.vn"
    default = return_tudongMSV()
    result = default + pre
    return result

class AddStudentForm(forms.Form):
    code = forms.CharField(label="Mã Sinh Viên", max_length=11, initial=return_tudongMSV, disabled=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Tài Khoản", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật Khẩu", min_length=5, max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control",'id':'password'}))
    confirm_password = forms.CharField(label="Xác Nhận Mật Khẩu", min_length=5, max_length=50,
                                       widget=forms.PasswordInput(attrs={"class": "form-control",'id':'confirm_password'}))

    def clean(self):
        valpwd = self.cleaned_data['password']
        valrpwd = self.cleaned_data['confirm_password']
        if valpwd != valrpwd:
            raise forms.ValidationError('Mật khẩu không khớp')

    email = forms.EmailField(label="Địa Chỉ Email", max_length=50, initial=return_tudongEmailSV, disabled=True,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    first_name = forms.CharField(label="Tên", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control",'id':'name1','onChange':'checkName1(this)'}))
    last_name = forms.CharField(label="Họ", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control",'id':'name','onChange':'checkName(this)'}))

    address = forms.CharField(label="Địa Chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    cmnd = forms.CharField(label="Chứng Minh Nhân Dân", min_length=9,max_length=11, widget=forms.NumberInput(attrs={"class": "form-control",'id':'cmnd'}))

    gender_list = (
        ('Nam','Nam'),
        ('Nữ','Nữ')
    )
    gender = forms.ChoiceField(label="Giới Tính", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    nienkhoa = forms.IntegerField(label="Niên Khóa", min_value=2018, max_value=2050,
                                  widget=forms.NumberInput(attrs={"class": "form-control",'id':'nienkhoa'}))

    profile_pic = forms.FileField(label="Ảnh Chân Dung 4*6", required=False, widget=forms.FileInput(attrs={"class":"form-control",'id':'fileImage'}))
    birthday = forms.DateField(label="Ngày Sinh", required=False, widget=forms.DateInput(attrs={"class":"form-control",'type': 'date','id':'birthday', 'onchange':'checkDate()'}))

class EditStudentForm(forms.Form):
    code = forms.CharField(label="Mã Sinh Viên", max_length=11, initial=return_tudongMSV, disabled=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, initial=return_tudongEmailSV, disabled=True,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Họ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control",'id':'name1','onChange':'checkName1(this)'}))
    last_name = forms.CharField(label="Tên", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control",'id':'name','onChange':'checkName(this)'}))
    username = forms.CharField(label="Tài Khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Địa Chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    cmnd = forms.CharField(label="Chứng Minh Nhân Dân", min_length=9, max_length=11,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    )

    gender = forms.ChoiceField(label="Giới Tính", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Ảnh Chân Dung", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control",'id':'fileImage'}))



    birthday = forms.DateField(label="birthday", required=False, widget=forms.DateInput(attrs={"class":"form-control",'type': 'date'}))

def return_tudongMGV():
    prefix = "gv"
    timestamp = str(int(time.time()) % 1624)
    default_value = prefix + timestamp
    return default_value


def return_tudongEmail():
    pre = "@teacher.ptithcm.edu.vn"
    default = return_tudongMGV()
    result = default + pre
    return result
class AddTeacherForm(forms.Form):
    code = forms.CharField(label="Mã Giáo Viên", max_length=11, initial=return_tudongMGV, disabled=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Tài Khoản", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật Khẩu", min_length=5, max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control",'id':'password','onChange':'checkPasswordStrength()'}))
    password1 = forms.CharField(label="Nhập Lại Mật Khẩu", min_length=5, max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control",'id':'password1'}))
    email = forms.CharField(label="Email", max_length=50, initial=return_tudongEmail, disabled=True,
                            widget=forms.TextInput(attrs={"class": "form-control"}))

    first_name = forms.CharField(label="Họ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control",'id':'name1','onChange':'checkName1(this)'}))
    last_name = forms.CharField(label="Tên", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control",'id':'name','onChange':'checkName(this)'}))
    cmnd = forms.CharField(label="Chứng Minh Nhân Dân", min_length=9,max_length=11, widget=forms.TextInput(attrs={"class": "form-control"}))

    address = forms.CharField(label="Địa Chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    )
    gender = forms.ChoiceField(label="Giới Tính", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Hình Ảnh", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control",'id':'fileImage'}))
    birthday = forms.DateField(label="Ngày Sinh", required=False,
                               widget=forms.DateInput(attrs={'class': 'form-control','type': 'date','id':'birthday','onchange':'checkDate()'}))
    salary = forms.CharField(label="Lương", max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))





class EditTeacherForm(forms.Form):
    username = forms.CharField(label="Tài Khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật Khẩu", min_length=5, max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    first_name = forms.CharField(label="Họ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control",'id':'name1','onChange':'checkName1(this)'}))
    last_name = forms.CharField(label="Tên", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control",'id':'name','onChange':'checkName(this)'}))
    cmnd = forms.CharField(label="Chứng Minh Nhân Dân", min_length=9,max_length=11, widget=forms.TextInput(attrs={"class": "form-control"}))

    address = forms.CharField(label="Địa Chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    )
    gender = forms.ChoiceField(label="Giới Tính", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Hình Ảnh", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control",'id':'fileImage'}))
    birthday = forms.DateField(label="Ngày Sinh", required=False,
                               widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))


def return_tudongMGVHP():
    prefix = "gvhp"
    timestamp = str(int(time.time()) % 1624)
    default_value = prefix + timestamp
    return default_value


def return_tudongEmailGVHP():
    pre = "@teacher.ptithcm.edu.vn"
    default = return_tudongMGVHP()
    result = default + pre
    return result


class AddTeacher_GVForm(forms.Form):
    code = forms.CharField(label="Mã Giáo Viên", max_length=11, initial=return_tudongMGVHP, disabled=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Tài Khoản", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật Khẩu", min_length=5, max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control",'id':'txtPassword'}))
    email = forms.EmailField(label="Email", max_length=50, initial=return_tudongEmailGVHP, disabled=True,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    first_name = forms.CharField(label="Họ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control",'id':'name1','onChange':'checkName1(this)'}))
    last_name = forms.CharField(label="Tên", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control",'id':'name','onChange':'checkName(this)'}))

    address = forms.CharField(label="Địa Chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    )

    gender = forms.ChoiceField(label="Giới Tính", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    cmnd = forms.CharField(label="Chứng Minh Nhân Dân", min_length=9, max_length=11,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Hình Ảnh", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control",'id':'fileImage'}))
    birthday = forms.DateField(label="Ngày Sinh", required=False,
                               widget=forms.DateInput(attrs={"class": "form-control",'type': 'date'}))



class EditTeacher_GVForm(forms.Form):
    code = forms.CharField(label="Mã Giáo Viên", max_length=11, initial=return_tudongMGVHP, disabled=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Tài Khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật Khẩu", min_length=5, max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, initial=return_tudongEmailGVHP, disabled=True,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    first_name = forms.CharField(label="Họ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control",'id':'name1','onChange':'checkName1(this)'}))
    last_name = forms.CharField(label="Tên", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control",'id':'name','onChange':'checkName(this)'}))

    address = forms.CharField(label="Địa Chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    )
    gender = forms.ChoiceField(label="Giới Tính", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    cmnd = forms.CharField(label="Chứng Minh Nhân Dân", min_length=9,max_length=11, widget=forms.TextInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Hình Ảnh", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control",'id':'fileImage'}))

    birthday = forms.DateField(label="Ngày Sinh", required=False,
                               widget=forms.DateInput(attrs={"class": "form-control",'type': 'date'}))
