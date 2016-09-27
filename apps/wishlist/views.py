from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from . import models
from ..logreg.models import Users

# Create your views here.
def index(request):
	user = Users.objects.get(id=request.session['user'])
	mywishlist = models.Wishlists.objects.filter(user=user)
	theirwishlist = models.Wishitems.objects.theirwishlist(user=user, mywishlist=mywishlist)
	context={'user':user, 'mywishlist':mywishlist, 'theirwishlist':theirwishlist}
	return render(request, 'wishlist/index.html', context)

def new(request):
	return render(request, 'wishlist/create.html')

def create(request):
	user = Users.objects.get(id=request.session['user'])
	item = request.POST['newProduct']
	itemcreate = models.Wishitems.objects.verify(user=user, item=item)
	if not itemcreate[0]:
		messages.error(request, itemcreate[1])
		return redirect(reverse('wishlist:wishlist_new'))
	models.Wishlists.objects.create(user=user, item=itemcreate[1])
	return redirect(reverse('wishlist:wishlist_index'))

def add(request, itemID):
	user = Users.objects.get(id=request.session['user'])
	item = models.Wishitems.objects.get(id=itemID)
	models.Wishlists.objects.create(user=user, item=item)
	return redirect(reverse('wishlist:wishlist_index'))

def show(request, itemID):
	item = models.Wishitems.objects.get(id=itemID)
	users = models.Wishlists.objects.filter(item=item)
	context = {'item':item, 'users':users}
	return render(request, 'wishlist/wish_item.html', context)

def remove(request, itemID):
	user = Users.objects.get(id=request.session['user'])
	item = models.Wishitems.objects.get(id=itemID)
	remover = models.Wishlists.objects.remove(user=user, item=item)
	if remover:
		item.delete()
	return redirect('wishlist:wishlist_index')
