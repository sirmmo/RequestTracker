from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.template import RequestContext
from django.forms import CheckboxSelectMultiple
from django.forms import RadioSelect
from django.forms import NullBooleanSelect
import json
from core.models import *

def index (request):
	if request.user.username:
		return render_to_response('index.html', {'know_user':True, 'username':request.user.username})
	else:
		return render_to_response('index.html', {'know_user':False})		

class RequestForm(ModelForm):
#	pub_date = DateField(label='Data di invio')
	class Meta:
		model = Request
		exclude = ('requester')

class ResponseForm(ModelForm):
	class Meta:
		model = Response
		exclude = ("request")
		widgets = {
			'dissatisfaction_reason': CheckboxSelectMultiple(),
			'satisfaction_level': RadioSelect(),
			'legal_support': NullBooleanSelect(),
			'legal_pursue': NullBooleanSelect(),
			'legal_ack': NullBooleanSelect(),
			'legal_ent': NullBooleanSelect(),
        }

class ProfileForm(ModelForm):
	class Meta:
		model = Requester
		exclude = ('user')

@login_required
def req_list(request):
	request_list = Request.objects.filter(requester__user = request.user).all()
	return render_to_response("requests.html", {'requests':request_list, 'know_user':True, 'username':request.user.username})
    
@login_required
def req_edit(request, id=None):
	if request.method == 'POST': # If the form has been submitted...
		form = RequestForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			req = form.save(commit=False)
			if id is not None:
				req.id = id
			req.requester = Requester.objects.get(user = request.user)
			req.save()
			return HttpResponseRedirect('/requests') # Redirect after POST
	else:
		if id is None:
			form = RequestForm() # An unbound form
		else:
			i = Request.objects.get(id=id)
			form = RequestForm(instance=i)
	c = RequestContext(request, {
    	'form': form,
    	'know_user':True, 
    	'username':request.user.username,
	'dates':['submission_date']
	})
	return render_to_response('form.html',c)
	
@login_required
def res_edit(request, id):
	if request.method == 'POST': # If the form has been submitted...
		form = ResponseForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			res = form.save(commit=False)
			res.id = id
			res.request = Request.objects.get(id = id)
			res.save()
			return HttpResponseRedirect('/requests') # Redirect after POST
	else:
		if id is None:
			form = ResponseForm() # An unbound form
		else:
			try:
				i = Response.objects.get(request__id=id)
				form = ResponseForm(instance = i) # An unbound form
			except:
				form = ResponseForm()

		
	c = RequestContext(request, {
    	'form': form,
    	'know_user':True, 
    	'username':request.user.username,
	'dates':['response_date']

	})
	return render_to_response('form.html',c)
	

@login_required
def req_info(request, id):
	req = Request.objects.get(id = id)
	return render_to_response("view.html", {'req':req, 'know_user':True, 'username':request.user.username})
	
@login_required
def res_info(request, id):
	req = Request.objects.get(id = id)
	return render_to_response("view.html", {'req':req, 'know_user':True, 'username':request.user.username})

@login_required
def req_delete(request, id):
	request_list = Request.objects.filter(requester__user = request.user).all()
	return render_to_response("form.html", {'requests':request_list, 'know_user':True, 'username':request.user.username})

def req_add_response(request, id):
	request_list = Request.objects.filter(requester__user = request.user).all()
	return render_to_response("form.html", {'requests':request_list, 'know_user':True, 'username':request.user.username})

@login_required
def prof_edit(request, username):
	if request.method == 'POST': # If the form has been submitted...
		form = ProfileForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			res = form.save(commit=False)
			if Requester.objects.filter(user = request.user).count() > 0:
				res.id = Requester.objects.get(user = request.user).id
			res.user = request.user
			res.save()
			return HttpResponseRedirect('/requests') # Redirect after POST
	else:
		if username is None:
			form = ProfileForm() # An unbound form
		else:
			try:
				i = Requester.objects.get(user = request.user)
				form = ProfileForm(instance = i) # An unbound form
			except:
				form = ProfileForm()

		
	c = RequestContext(request, {
    	'form': form,
    	'know_user':True, 
    	'username':request.user.username
	})
	return render_to_response('form.html',c)
	

def req_stats(request):
	r = []
	for req in Request.objects.all():
		req_ = {}
		req_['user'] = str(req.requester)
		req_['organization'] = str(req.requester.organization)
		req_['submission_date'] = str(req.submission_date)
		req_['topic'] = str(req.topic)
		req_['level'] = str(req.level)
		try:
			t = req.response
			req_['has_response'] = True
			req_['satisfaction_level']= str(req.response.satisfaction_level)
			req_['response_date'] = str(req.response.response_date)
		except:
			req_['has_response'] = False
		r.append(req_)

	return HttpResponse(json.dumps(r))
