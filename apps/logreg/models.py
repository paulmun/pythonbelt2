from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from django.db.models import Count

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')

class UserManager(models.Manager):
	def register(self, **kwargs):
		errors = {}
		
		fname = kwargs['fname']
		lname = kwargs['lname']
		email = kwargs['email']
		password = kwargs['password']
		cpassword = kwargs['cpassword']
		bday = kwargs['bday']
		hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		
		if NAME_REGEX.match(fname) or len(fname) < 3:
			errors['fname'] = 'Please enter a valid first name.'
		if NAME_REGEX.match(lname) or len(fname) < 3:
			errors['lname'] = 'Please enter a valid last name.'
		if not EMAIL_REGEX.match(email):
			errors['email'] = 'Please enter a valid email.'
		elif self.filter(email=email):
			errors['email'] = 'This email is already in use!'
		if len(password) < 8:
			errors['password'] = 'Password must be at least 8 characters long'
		elif not password == cpassword:
			errors['password'] = 'Your passwords do not match.'
		elif not bday:
			errors['bday'] = 'Please enter your birthday!'
		if errors:
			return (False, errors)
		else:
			newUser = self.create(fname=fname, lname=lname, email=email, password=hashed, bday=bday)
			return (True, newUser.id)

	def login(self, **kwargs):
		errors = {}
		email = kwargs['email']
		password = kwargs['password']
		try:
			user = self.get(email=email)
		except:
			errors['email'] = 'The email you entered does not exist'
			return(False, errors)
		hashed = bcrypt.hashpw(password.encode(), user.password.encode())
		if not EMAIL_REGEX.match(email):
			errors['email'] = 'Please enter a valid email'
		elif not user:
			errors['email'] = 'Could not find an account for '+email
		elif not user.password == hashed: 
			errors['password'] = 'Invalid email or password'
		else:
			return (True, user.id)
		return (False, errors)

	def everyoneElse(self, id):
		return self.exclude(id=id).annotate(history=Count('pokee'))
			

class Users(models.Model):
	fname = models.CharField(max_length=45)
	lname = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	password = models.CharField(max_length=80)
	bday = models.DateField(auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
