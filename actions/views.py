from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import AllUsers
# Create your views here.


@csrf_exempt
def login_page(request):
    return render(request, 'login.html')


@csrf_exempt
def login_auth(request):
    postdata = request.POST
    print(postdata)
    if 'username' and 'password' in postdata:
        print(postdata['username'])
        print(postdata['password'])
        user = authenticate(username=postdata['username'], password=postdata['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = postdata['username']
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
    page_title = '|Home|'
    user = request.session['user']
    if not AllUsers.objects.exists():
        print(request.session['user'])
        new_user = AllUsers(username=user, Name=user, Email=user+'@inflack.com', Admin=True)
        new_user.save()

    if AllUsers.objects.filter(username__exact=user).exists():
        admin_user = AllUsers.objects.get(username__exact=user)
        admin_admin = admin_user.Admin
        login_user = admin_user.Name
        if admin_user.Active:
            display = render(request, 'client_dashboard.html', {'loggedInUser': login_user,
                                                                'page_title': page_title,
                                                                'admin_admin': admin_admin})
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


    # @login_required(login_url='/login/')
    # def add_employee(request):
    #     user = request.session['user']
    #     post_data = request.POST
    #     # print(post_data['super-admin'])
    #     if 'username' in post_data and 'csrfmiddlewaretoken' in post_data:
    #         # if admin
    #         if AllUsers.objects.filter(username__exact=user).exists():
    #             admin_user = AllUsers.objects.get(username__exact=user)
    #             admin_admin = admin_user.Admin
    #             loggedInUser = admin_user.Name
    #             if admin_user.Active and admin_admin:
    #                 if AdminUser.objects.filter(username__exact=post_data['username']).exists() or \
    #                         ClientUser.objects.filter(username__exact=post_data['username']).exists():
    #                     display = render(request, 'add_admin.html',
    #                                      {'wrong': True,
    #                                       'text': 'Username already taken. Please try with a different username.',
    #                                       'admin': admin,
    #                                       'loggedInUser': loggedInUser,
    #                                       'admin_admin': admin_admin})
    #                 else:
    #                     if post_data['re-password'] == post_data['password']:
    #                         new_admin_username = post_data['username']
    #                         new_admin_name = post_data['name']
    #                         new_admin_phone = post_data['phone']
    #                         new_admin_email = post_data['email']
    #                         if 'super-admin' in post_data and post_data['super-admin'] == 'on':
    #                             new_admin_super_admin = True
    #                         else:
    #                             new_admin_super_admin = False
    #                         new_admin_password = post_data['password']
    #                         new_added_admin = AdminUser(username=new_admin_username,
    #                                                     Name=new_admin_name,
    #                                                     Email=new_admin_email,
    #                                                     Admin=new_admin_super_admin,
    #                                                     Phone=new_admin_phone)
    #                         new_added_admin.save()
    #                         new_user = User.objects.create_user(new_admin_username,
    #                                                             new_admin_email,
    #                                                             new_admin_password)
    #                         new_user.save()
    #                         display = render(request, 'add_admin.html',
    #                                          {'wrong': True,
    #                                           'loggedInUser': loggedInUser,
    #                                           'text': 'The new user is added successfully',
    #                                           'admin': admin,
    #                                           'admin_admin': admin_admin})
    #                     else:
    #                         display = render(request, 'add_admin.html',
    #                                          {'wrong': True,
    #                                           'loggedInUser': loggedInUser,
    #                                           'text': 'Passwords do not match. Please Try Again.',
    #                                           'admin': admin,
    #                                           'admin_admin': admin_admin})
    #             else:
    #                 logout(request)
    #                 display = render(request, 'login.html',
    #                                  {'wrong': True,
    #                                   'text': 'You are not authorized to login.'
    #                                           ' Please contact administrator for more details'})
    #         else:
    #             display = redirect('/')
    #     else:
    #         display = redirect('/add_admin/')
    #     return display