from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import AllUsers, ACL
from status.models import Status
from task.models import Task
import datetime
from attendance.models import AttendanceInOffice, AttendanceInHome

from django.contrib.auth.models import User

# Create your views here.


@csrf_exempt
def login_page(request):
    return render(request, 'login.html')


@csrf_exempt
def login_auth(request):
    post_data = request.POST
    print(post_data)
    if 'username' and 'password' in post_data:
        print(post_data['username'])
        print(post_data['password'])
        user = authenticate(username=post_data['username'], password=post_data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = post_data['username']
                if user.is_superuser:
                    res = redirect('/admin')
                else:
                    res = redirect('/')
            else:
                res = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'The password is valid, but the account has been disabled!'})
        else:
            res = render(request, 'login.html',
                         {'wrong': True,
                          'text': 'The username and password you have entered is not correct. Please retry'})
    else:
        res = render(request, 'login.html', {'wrong': False})

    res['Access-Control-Allow-Origin'] = "*"
    res['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    res['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
    return res


def logout_now(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login/')
def home(request):
    page_title = 'Home'
    user = request.session['user']
    if not AllUsers.objects.exists():
        print(request.session['user'])
        new_status = Status.objects.get(StatusKey='office')
        new_user = AllUsers(username=user, Name=user, Email=user + '@inflack.com', Status=new_status)
        new_user.save()
        new_user_acl = ACL(user=new_user,
                           CanSeeOthersTaskList=True,
                           CanSeeOthersAttendance=True,
                           CanAddMoreEmployee=True,
                           CanSeeOthersDetails=True,
                           CanSeeOthersStatus=True)
        new_user_acl.save()
    if AllUsers.objects.filter(username__exact=user).exists():
        this_user = AllUsers.objects.get(username__exact=user)
        if this_user.Active:
            all_status = Status.objects.all()
            display = render(request, 'client_dashboard.html', {'login_user': this_user,
                                                                'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                                'can_add_employee': this_user.acl.CanAddMoreEmployee,
                                                                'all_status': all_status,
                                                                'page_title': page_title})
        else:
            logout(request)
            display = render(request, 'login.html',
                             {'wrong': True,
                              'text': 'You are not authorized to login. Please contact administrator for more details'})
    else:
        logout(request)
        display = render(request, 'login.html',
                         {'wrong': True,
                          'text': 'Something went wrong. Please LOGIN again.'})
    return display


@login_required(login_url='/login/')
def add_employee(request):
    user = request.session['user']
    post_data = request.POST
    this_user = AllUsers.objects.get(username__exact=user)
    # login_user = this_user.Name
    # print(post_data['super-admin'])
    if 'username' in post_data and 'csrfmiddlewaretoken' in post_data:
        if AllUsers.objects.filter(username__exact=user).exists():
            if this_user.Active and this_user.acl.CanAddMoreEmployee:
                if AllUsers.objects.filter(username__exact=post_data['username']).exists() or \
                                post_data['username'] == 'admin':
                    # This username is already taken
                    print(post_data)
                    display = render(request, 'add_admin.html', {'page_title': 'Add Employee',
                                                                 'login_user': this_user,
                                                                 'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                                 'can_add_employee': this_user.acl.CanAddMoreEmployee,
                                                                 'wrong': True,
                                                                 'text': 'This USERNAME is already taken.'
                                                                         'Please try with a different one'})
                else:
                    if post_data['password'] == post_data['re-password']:
                        # password matches
                        print(post_data)
                        new_status = Status.objects.get(StatusKey='office')
                        new_user = AllUsers(username=post_data['username'],
                                            Name=post_data['name'],
                                            Designation=post_data['designation'],
                                            Phone=post_data['phone'],
                                            Email=post_data['email'],
                                            Status=new_status)
                        new_user.save()
                        new_user_acl = ACL(user=new_user)
                        new_user_acl.save()
                        new_user_login = User.objects.create_user(post_data['username'],
                                                                  post_data['email'],
                                                                  post_data['password'])
                        new_user_login.save()
                        display = render(request, 'add_admin.html', {'page_title': 'Add Employee',
                                                                     'login_user': this_user,
                                                                     'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                                     'can_add_employee': this_user.acl.CanAddMoreEmployee,
                                                                     'success': True,
                                                                     'text': 'New employee has been '
                                                                             'added successfully.'})
                    else:
                        display = render(request, 'add_admin.html', {'page_title': 'Add Employee',
                                                                     'login_user': this_user,
                                                                     'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                                     'can_add_employee': this_user.acl.CanAddMoreEmployee,
                                                                     'wrong': True,
                                                                     'text': 'The passwords do not match.'
                                                                             'Please try again'})
            else:
                logout(request)
                display = render(request, 'login.html',
                                 {'wrong': True,
                                  'text': 'You are not authorized to login.'
                                          ' Please contact administrator for more details'})
        else:
            display = redirect('/')
    else:
        if this_user.acl.CanAddMoreEmployee:
            display = render(request, 'add_admin.html', {'page_title': 'Add Employee',
                                                         'login_user': this_user,
                                                         'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                         'can_add_employee': this_user.acl.CanAddMoreEmployee})
        else:
            display = render(request, 'access_denied.html', {'page_title': 'Add Employee',
                                                             'login_user': this_user,
                                                             'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                             'can_add_employee': this_user.acl.CanAddMoreEmployee})
    return display


@login_required(login_url='/login/')
def change_status(request):
    user = request.session['user']
    get_data = request.GET
    if AllUsers.objects.filter(username__exact=user).exists():
        new_status = Status.objects.get(StatusKey=get_data['to'])
        this_user = AllUsers.objects.get(username__exact=user)
        current_status = this_user.Status
        print(current_status.StatusKey)
        print(get_data['to'])

        if ((get_data['to'] == 'office' or get_data['to'] == 'away' or
                     get_data['to'] == 'meeting' or get_data['to'] == 'out') and current_status.StatusKey != 'home') or \
                                get_data['to'] == 'home' and current_status.StatusKey == 'out' or \
                                get_data['to'] == 'out' and current_status.StatusKey == 'home':
            if (get_data['to'] == 'office' or get_data['to'] == 'away' or get_data['to'] == 'meeting') \
                    and current_status.StatusKey == 'out':
                new_office_attendance = AttendanceInOffice(User=this_user)
                new_office_attendance.save()
            elif get_data['to'] == 'home'and current_status.StatusKey == 'out':
                new_home_attendance = AttendanceInHome(User=this_user)
                new_home_attendance.save()
            elif get_data['to'] == 'out'and current_status.StatusKey == 'home':
                new_home_attendance = AttendanceInHome.objects.get(User=this_user, ExitTime=None)
                print(datetime.datetime.now())
                new_home_attendance.ExitTime = datetime.datetime.now()
                new_home_attendance.save()
            elif get_data['to'] == 'out'and (current_status.StatusKey == 'office' or
                                                     current_status.StatusKey == 'away' or
                                                     current_status.StatusKey == 'meeting'):
                new_office_attendance = AttendanceInOffice.objects.get(User=this_user, ExitTime=None)
                print(datetime.datetime.now())
                new_office_attendance.ExitTime = datetime.datetime.now()
                new_office_attendance.save()
            this_user.Status = new_status
            this_user.save()
        display = redirect('/')
    else:
        display = redirect('/logout')
    return display


@login_required(login_url='/login/')
def employee_list(request):
    user = request.session['user']
    if AllUsers.objects.filter(username__exact=user).exists():
        this_user = AllUsers.objects.get(username__exact=user)
        if this_user.acl.CanSeeOthersStatus:
            all_employees = AllUsers.objects.all()
            display = render(request, 'admin_list.html', {'page_title': 'Add Employee',
                                                          'login_user': this_user,
                                                          'all_employees': all_employees,
                                                          'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                          'can_add_employee': this_user.acl.CanAddMoreEmployee})
        else:
            display = render(request, 'access_denied.html', {'page_title': 'Add Employee',
                                                             'login_user': this_user,
                                                             'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                             'can_add_employee': this_user.acl.CanAddMoreEmployee})
    else:
        display = redirect('/logout')
    return display


@login_required(login_url='/login/')
def all_task(request):
    user = request.session['user']
    if AllUsers.objects.filter(username__exact=user).exists():
        this_user = AllUsers.objects.get(username__exact=user)
        # if this_user.acl.CanSeeOthersStatus:
        all_tasks = Task.objects.filter(AssignedTo=this_user)
        assigned_tasks = Task.objects.filter(AssignedBy=this_user)
        display = render(request, 'all_task.html', {'page_title': 'Task List',
                                                    'login_user': this_user,
                                                    'all_tasks': all_tasks,
                                                    'assigned_tasks': assigned_tasks,
                                                    'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                    'can_add_employee': this_user.acl.CanAddMoreEmployee})
    else:
        display = redirect('/logout')
    return display


@login_required(login_url='/login/')
def attendance(request):
    user = request.session['user']
    if AllUsers.objects.filter(username__exact=user).exists():
        this_user = AllUsers.objects.get(username__exact=user)
        # if this_user.acl.CanSeeOthersStatus:
        office_work = AttendanceInOffice.objects.filter(User=this_user)
        home_work = AttendanceInHome.objects.filter(User=this_user)
        display = render(request, 'attendance.html', {'page_title': 'Attendance',
                                                      'login_user': this_user,
                                                      'office_work': office_work,
                                                      'home_work': home_work,
                                                      'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                      'can_add_employee': this_user.acl.CanAddMoreEmployee})
    else:
        display = redirect('/logout')
    return display


@login_required(login_url='/login/')
def profile(request):
    user = request.session['user']
    if AllUsers.objects.filter(username__exact=user).exists():
        this_user = AllUsers.objects.get(username__exact=user)
        display = render(request, 'profile.html', {'page_title': 'Profile',
                                                   'login_user': this_user,
                                                   'this_user': this_user,
                                                   'can_see_others_status': this_user.acl.CanSeeOthersStatus,
                                                   'can_add_employee': this_user.acl.CanAddMoreEmployee})
    else:
        display = redirect('/logout')
    return display


