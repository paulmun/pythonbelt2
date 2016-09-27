from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
	context={'users': models.Users.objects.all()}
	return render(request, 'logreg/index.html', context)

def register(request):
	fname = request.POST['fname']
	lname = request.POST['lname']
	email = request.POST['email']
	bday = request.POST['bday']
	newUser = models.Users.objects.register(fname=fname, lname=lname, email=email, password=request.POST['pass'], cpassword=request.POST['cPass'], bday=bday)
	print newUser
	if newUser[0]:
		request.session['user']=newUser[1]
		return redirect(reverse('poke:poke_index'))
	else:
		context = {'errors':newUser[1], 'fname':fname, 'lname':lname, 'email':email}
		return render(request, 'logreg/index.html', context)

def login(request):
	user = models.Users.objects.login(email=request.POST['email'], password=request.POST['pass'])
	if user[0]:
		request.session['user'] = user[1]
		return redirect(reverse('poke:poke_index'))
	else:
		context = {'errors2':user[1]}
		return render(request, 'logreg/index.html', context)

def logout(request):
	request.session.clear()
	return redirect('logreg:logreg_index')
	