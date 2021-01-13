from _ctypes_test import func
from functools import wraps

from django.contrib.messages.storage import session
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import ModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from App import models
from App.models import User, LeavingMessage, Position, Department, CompanyNotice


# 博客首页
def index(request):
    query = request.GET.get('top-search', '')
    users = User.objects.all().filter(email__contains=query)
    # 实例化结果集，定义每页5条数据
    paginator = Paginator(users, 10)
    # 获取get请求的page值
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', context={'users': contacts})


# 用户登录页面
def login(request):
    if request.method == 'POST':
        # 获取用户提交的数据
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 通过获取的email,password来查看数据库中是否有此用户存在
        user_obj = models.User.objects.filter(email=email, password=password).first()

        if user_obj:
            # 如果用户存在，那么使用此用户对象拿到此用户的用户名
            username = user_obj.username
            # 设置session
            request.session['is_login'] = True
            # 将刚刚拿到的用户名存入session中
            request.session['username'] = username
            request.session['pk'] = user_obj.pk
            return redirect('/user/index')
        error = 'Wrong email or password'
    return render(request, 'login.html', locals())
###########
# 退出登录 #
###########
def login_out(request):
    del request.session['is_login']
    del request.session['username']
    return redirect('/user/login')


# 用户注册页面


def user_register(request):
    positions = Position.objects.all()
    departments = Department.objects.all()

    if request.method == 'POST':
        # 获取用户注册信息
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        department_id = request.POST.get('department_id')
        position_id = request.POST.get('position_id')

        # 获取所有的对象列表
        users = User.objects.all()
        if not users.filter(email=email):
            # 如果数据库中不存在此邮箱，那么就验证输入的密码是否一致
            if password == repassword:
                # 如果密码一致，则添加数据到数据库
                User.objects.create(email=email, username=username, password=password, position_id=position_id,
                                    department_id=department_id)
                return redirect('/user/login/')
            else:
                return render(request, 'user_register.html',
                              context={'msg': '两次输入密码不一致', 'positions': positions, 'departments': departments})
        else:
            return render(request, 'user_register.html',
                          context={'msg': '邮箱已被注册', 'positions': positions, 'departments': departments})

    return render(request, 'user_register.html', context={'positions': positions, 'departments': departments})


# 用户删除页面
def del_user(request):
    # 获取要删除的用户的id
    uid = request.GET.get('uid')
    # 在数据库中查找用户对象
    user = User.objects.get(id=uid)
    # 删除用户
    user.delete()

    return redirect('/user/index/')


# 修改用户信息
def update_user(request):
    uid = request.GET.get('uid')
    user = User.objects.get(id=uid)
    positions = Position.objects.all()
    departments = Department.objects.all()

    if not request.method == 'GET':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        position_id = request.POST.get('position_id')
        department_id = request.POST.get('department_id')
        # 修改原有信息
        user.email = email
        user.username = username
        user.password = password
        user.address = address
        user.position_id = position_id
        user.department_id = department_id
        # 提交到数据库
        user.save()
        return redirect('/user/index/')
    else:
        return render(request, 'update_user.html',
                      context={'user': user, 'positions': positions, 'departments': departments})


# 展示员工留言
def show_leavingmessage(request):
    # 查询所有的留言
    all_message = LeavingMessage.objects.all().order_by('-addtime')

    comments = models.Comment.objects.all()
    # 实例化结果集，定义每页5条数据
    paginator = Paginator(all_message, 10)
    # 获取get请求的page值
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'leavingmessage.html', context={'contacts': contacts, 'comments': comments})


# 员工发表留言
def add_leavingmessage(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        username = request.session.get('username')
        user_obj = models.User.objects.get(username=username)
        user_id = user_obj.pk

        if len(content) > 200:
            return redirect('/user/addleavingmessage', context={'msg': '输入内容不能超过200字'})
        else:
            LeavingMessage.objects.create(content=content, user_id=user_id)
            return redirect('/user/showleavingmessage')

    return render(request, 'addleavingmessage.html')


# 删除留言
def del_message(request):
    # 获取用户id以及要删除的留言id
    user_id = request.GET.get('uid')
    message_id = request.GET.get('messageid')
    message = LeavingMessage.objects.filter(user=user_id, pk=message_id)
    message.delete()
    return redirect('/user/showleavingmessage/')


# 公司通告展示页面
def com_circular(request):
    notices = models.CompanyNotice.objects.all().order_by('-addtime')
    # 实例化结果集，定义每页5条数据
    paginator = Paginator(notices, 5)
    # 获取get请求的page值
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'companycircular.html', context={'contacts': contacts})


# 发布公司通告
def addcircular(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        username = request.session.get('username')
        user_obj = models.User.objects.get(username=username)
        user_id = user_obj.pk
        models.CompanyNotice.objects.create(content=content, user_id=user_id)
        return redirect('/user/showcircular')

    return render(request, 'addcircular.html')

# 删除公司通告
def del_notice(request):
    # 获取用户id以及要删除的留言id
    user_id = request.GET.get('uid')
    notice_id = request.GET.get('noticeid')
    notice = CompanyNotice.objects.filter(user=user_id, pk=notice_id)
    notice.delete()
    return redirect('/user/showcircular/')


def comment(request):
    content = request.POST.get('comment')
    user_id = request.session.get('pk')
    leavingmessage_id = request.GET.get('pk')

    models.Comment.objects.create(content=content, user_id=user_id, leavingmessage_id=leavingmessage_id)
    return redirect('/user/showleavingmessage/')


def leave_list(request):

    all_users = models.User.objects.all()
    return render(request, 'leave_list.html', {'all_users': all_users})

class UserForm(ModelForm):
    class Meta:
        model = models.User
        fields = ['status']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # 自定义的操作
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

def leave_edit(request):
    uid = request.GET.get('uid')
    obj = models.User.objects.filter(pk=uid).first()
    userform = UserForm(instance=obj)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=obj)
        if userform.is_valid():
            userform.save()
            return redirect('/user/leave_list/')
    return render(request, 'leave_edit.html', {'userform':userform})


# 申请请假
def apply(request):

    if request.method == 'POST':
        user_id = request.POST.get('pk')
        reason = request.POST.get('reason')
        status = False
        models.ApplyLeave.objects.create(user_id=user_id, reason=reason, status=status)


        return redirect('/user/apply_leave/')

    return render(request, 'apply.html')

# 展示所有请假申请
def apply_leave(request):
    applyleaves = models.ApplyLeave.objects.all().order_by('-applydate')

    return render(request, 'apply_leave.html', {'applyleaves': applyleaves})

# 批准请假
def approval(request):
    status = request.GET.get('status')
    pk = request.GET.get('applyid')
    apply_obj = models.ApplyLeave.objects.get(pk=pk)
    apply_obj.status = status
    apply_obj.save()
    return redirect('/user/apply_leave/')