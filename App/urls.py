# -*- coding = utf-8 -*-
# @Time : 2020/11/21 17:58
# @Author : Chenih
# @File : urls.py
# @Software : PyCharm


from django.urls import path

from App import views

app_name = 'App'  # 应用名空间，用来反向解析
urlpatterns = [
    path('index/', views.index, name='index'),                            # 首页
    path('login/', views.login, name='login'),                            # 用户登录
    path('loginout/', views.login_out, name='loginout'),                  # 退出登录
    path('userreg/', views.user_register, name='register'),               # 用户注册
    path('del/', views.del_user, name='del'),                             # 用户删除
    path('update/', views.update_user, name='update'),                    # 用户信息更新

    path('showleavingmessage/', views.show_leavingmessage, name='show'),  # 留言板展示
    path('addleavingmessage/', views.add_leavingmessage, name='add'),     # 发表留言
    path('delmessage/', views.del_message, name='delmessage'),            # 删除留言
    path('comment/', views.comment, name='comment'),                      # 留言评论表
    path('showcircular/', views.com_circular, name='circular'),           # 公司通告展示
    path('addcircular/', views.addcircular, name='addcircular'),           # 发布公司通告
    path('delnotice/', views.del_notice, name='delnotice'),                # 删除公司通告

    path('leave_list/', views.leave_list, name='leave_list'),              # 请假人员列表
    path('leave_edit/', views.leave_edit, name='leave_edit'),              # 管理员编辑请假
    path('apply_leave/', views.apply_leave, name='apply_leave'),            # 员工申请假期表
    path('apply/', views.apply, name='apply'),                               # 申请假期
    path('approval/', views.approval, name='approval')                       # 批准假期
]
