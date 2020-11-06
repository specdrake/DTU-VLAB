from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/anurag/Workspace/DTU/CourseProj/AE/website/DTU-VLAB/dtuvlab/lab/simulations/examples/diode')
import exp1 as diode
import matplotlib.pyplot as plt

def index(request):
    return render(request, "lab/index.html", {
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "lab/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lab/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lab/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "lab/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lab/register.html")

@login_required
def experiments(request):
    return render(request, "lab/experiments.html")

def exp(request, expnum):
    if request.method == 'POST':
        print("hello", expnum)
        tablerow = []
        if expnum == "1":
            print("Hello")
            print("res:----", request.POST["val-1res"])
            print("volt:----", request.POST["val-1dcvolt"])
            row = {}
            row['res']=request.POST["val-1res"] 
            row['vdc']=request.POST["val-1dcvolt"]
            print(row['res'])
            c = diode.init()
            diode.setCircuitParams(5, 1000, '1N4148', c)
            anl, tmp = diode.simulateTemp(c)
            canl = anl[25]

            print(anl)
            diode.plotFunc(c)
            print("Hello World!!!!")
            print("Hasdfd")
            # print(type(plot1))
            
            # plt.show()
            tablerow.append(row)
            
            return render(request, f"lab/exp{expnum}.html", {
                'expnum' : expnum,
                'mesg' : "Success1!",
                'tablerow' : tablerow
            })
        else:
            return HttpResponse("<h1>Error!</h1>")
    else:
        return render(request, f"lab/exp{expnum}.html", {
            'expnum' : expnum
        })