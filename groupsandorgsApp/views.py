from django.shortcuts import render, redirect
from .models import User, Org
import bcrypt
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    validationErrors = User.objects.registrationValidator(request.POST)
    print(validationErrors)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    hashedPW = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(email = request.POST['email'],firstName= request.POST['fname'], lastName=request.POST['lname'], password = hashedPW ) 
    request.session['loggedInUserID'] = newuser.id
    return redirect("/groups")


def login(request):
    loginerrors = User.objects.loginValidator(request.POST)
    if len(loginerrors)>0:
        for key, value in loginerrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        loggedinuser = User.objects.filter(email = request.POST['email'])
        loggedinuser = loggedinuser[0]
        request.session['loggedInUserID'] = loggedinuser.id
        return redirect("/groups")

def groups(request):
    loggedInUser = User.objects.get(id = request.session['loggedInUserID'])
    context = {
        'groupers': loggedInUser.groups.all(),
        'loggedinuser': loggedInUser,
        'allOrgs': Org.objects.all(),
        'myOrgs': Org.objects.filter(joiner = loggedInUser),
        'otherOrgs': Org.objects.exclude(joiner = loggedInUser)
    }
    return render(request, "groups.html", context)

def submitorg(request):
    print(request.POST)
    validationErrors = User.objects.orgValidator(request.POST)
    print(validationErrors)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/groups")
    loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
    neworg = Org.objects.create(orgname = request.POST['org'], description = request.POST['desc'],joiner= loggedinuser)
    print(request.POST)
    return redirect("/groups")


def groupinfo(request, orgID):
    loggedInUser = User.objects.get(id = request.session['loggedInUserID'])
    context = {
        'org': Org.objects.get(id = orgID),
        'groupers': loggedInUser.groups.all(),
        'loggedinuser': loggedInUser,
        'allOrgs': Org.objects.all(),
        'myOrgs': Org.objects.filter(joiner = loggedInUser),
        'otherOrgs': Org.objects.exclude(joiner = loggedInUser)
    }
    return render(request, "groupinfo.html", context)


def joingroup(request, orgID):
    loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
    orginfo = Org.objects.get(id= orgID)
    orginfo.group.add(loggedinuser)
    return redirect(f"/groups/{orgID}")

def leavegroup(request, orgID):
    loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
    orginfo = Org.objects.get(id= orgID)
    orginfo.group.remove(loggedinuser)
    return redirect(f"/groups/{orgID}")

def logout(request):
    request.session.clear()
    return redirect("/")

def dashboard(request):
    return redirect("/groups")



# def deleteorg(request, allOrgsID):
#     loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
#     orginfo = Org.objects.get(id= allOrgsID)
#     orginfo.group.remove(loggedinuser)
#     print(orginfo)
#     print('*****')
#     return redirect("/groups")
