from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.template import RequestContext
from django.forms import CheckboxSelectMultiple
from django.forms import RadioSelect, PasswordInput, HiddenInput
from django.forms import NullBooleanSelect
from django.utils.translation import ugettext_lazy as _
import json
from django import forms
from core.models import *
from django.utils.encoding import smart_str #as do_smart_str

#def smart_str(s):
#	return do_smart_str(s, encoding='utf-16', strings_only=False, errors='strict')

def index (request):
	if request.user.username:
		return render_to_response('index.html', {'know_user':True, 'is_index':True,  'username':request.user.username, 'superuser':request.user.is_superuser})
	else:
		return render_to_response('index.html', {'know_user':False})		

class RequestForm(ModelForm):
#	pub_date = DateField(label='Data di invio')
	class Meta:
		model = Request
		exclude = ('requester', 'code')

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
	return render_to_response("requests.html", {'requests':request_list, 'is_index':False, 'know_user':True, 'username':request.user.username, 'superuser':request.user.is_superuser})
    
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
	'dates':['submission_date'], 
	'superuser':request.user.is_superuser
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
	'dates':['response_date'], 
	'superuser':request.user.is_superuser

	})
	return render_to_response('form.html',c)
	

@login_required
def req_info(request, id):
	req = Request.objects.get(id = id)
	return render_to_response("view.html", {'req':req, 'know_user':True, 'is_index':False,'username':request.user.username, 'superuser':request.user.is_superuser})
	
@login_required
def res_info(request, id):
	req = Request.objects.get(id = id)
	return render_to_response("view.html", {'req':req, 'know_user':True, 'is_index':False,'username':request.user.username, 'superuser':request.user.is_superuser})

@login_required
def req_delete(request, id):
	request_list = Request.objects.filter(requester__user = request.user).all()
	return render_to_response("form.html", {'requests':request_list, 'is_index':False,'know_user':True, 'username':request.user.username, 'superuser':request.user.is_superuser})

def req_add_response(request, id):
	request_list = Request.objects.filter(requester__user = request.user).all()
	return render_to_response("form.html", {'requests':request_list, 'is_index':False,'know_user':True, 'username':request.user.username, 'superuser':request.user.is_superuser})

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
    	'username':request.user.username,
	'is_index':False,
	})
	return render_to_response('form.html',c)
	

def req_stats(request):
	r = []
	for req in Request.objects.all():
		req_ = {}
		req_['user'] = smart_str(req.requester)
		req_['organization'] = smart_str(req.requester.organization)
		req_['submission_date'] = smart_str(req.submission_date)
		req_['topic'] = smart_str(req.topic)
		req_['level'] = smart_str(req.level)
		try:
			t = req.response
			req_['has_response'] = True
			req_['satisfaction_level']= smart_str(req.response.satisfaction_level)
			req_['response_date'] = smart_str(req.response.response_date)
		except:
			req_['has_response'] = False
		r.append(req_)

	return HttpResponse(json.dumps(r))

class UserSelectForm(forms.Form):
	user = forms.CharField(max_length=100, label=_('Username'))

class UserResponseForm(forms.Form):
	user = forms.CharField(max_length=250, label=_('Username'), widget=HiddenInput())
	request = forms.CharField(max_length=500, label=_('Request'))
	response = forms.CharField(max_length=500, label=_('Response'))

class NewPasswordForm(forms.Form):	
	user = forms.CharField(max_length=250, label=_('Username'), widget=HiddenInput())
	request = forms.CharField(max_length=500, label=_('Request'), widget=HiddenInput())
	response = forms.CharField(max_length=500, label=_('Response'), widget=HiddenInput())
	password = forms.CharField(max_length=100, widget=PasswordInput(), label=_('New Password'))
	password_r = forms.CharField(max_length=100, widget=PasswordInput(), label=_('Repeat New Password'))


def lost_pw(request):
	u = request.REQUEST.get('user')
	r = request.REQUEST.get('response')
	p = request.REQUEST.get('password')
	p_r = request.REQUEST.get('password_r')

	if u is None and r is None and p is None:
		return render_to_response('form.html',RequestContext(request, {'form':UserSelectForm()}))
	elif u is not None and r is None and p is None:
		form = UserResponseForm(initial={'user':u, 'request':Requester.objects.get(user__username=u).security_question })
		return render_to_response('form.html',RequestContext(request, {'form':form}))
	elif u is not None and r is not None and p is None:
		if Requester.objects.get(user__username=u).security_answer == r:
			form = NewPasswordForm(initial={'user':u, 'response':r, 'request':Requester.objects.get(user__username=u).security_question })
			return render_to_response('form.html', RequestContext(request, {'form':form}))
		else:
			form = UserResponseForm(initial={'user':u, 'response':r, 'request':Requester.objects.get(user__username=u).security_question })
			return render_to_response('form.html',RequestContext(request, {'form':form}))
	elif u is not None and r is not None and p == p_r:
		u =User.objects.get(username=u)
		u.set_password(p)
		u.save()
		return HttpResponseRedirect('/')
	else:
		return render_to_response('form.html',{'form':UserSelectForm()})

	
import csv


@login_required
def req_csv(request):
	return do_req_csv(request.user)

def do_req_csv(user):
	req_s = Request.objects
	if user.is_superuser:
		pass
	else:
		req_s = req_s.filter(requester__user = user)
	arr = [
		'user',  
		'organization', 
		'code',
		'submission_date', 
		'topic',
		'level',
		'area', 
		'has_response',
		'response_date',
		'satisfaction_level',
		'dissatisfacion_reason',
		'ack',
		'transferred',
		'transferred_ack',
		'transferred_rereq',
		'payment',
		'legal_pursue',
		'legal_support', 
		 ]
	response = HttpResponse(mimetype="text/csv")
	writer = csv.writer(response)
	writer.writerow(arr)
	for req in req_s.all():
		req_ = {}
		req_['user'] = smart_str(req.requester)
		req_['code'] = smart_str(req.code)
		req_['organization'] = smart_str(req.requester.organization)
		req_['submission_date'] = smart_str(req.submission_date)
		req_['topic'] = smart_str(req.topic)
		req_['level'] = smart_str(req.level)
		req_['area'] = smart_str(req.area)
		try:
			t = req.response
			req_['has_response'] = True
			req_['response_date'] = smart_str(req.response.response_date)
			req_['satisfaction_level']= smart_str(req.response.satisfaction_level)
			req_['legal_support']= smart_str(req.response.legal_support)
			req_['ack']= smart_str(req.response.legal_ack)
			req_['transferred']= smart_str(req.response.legal_ent)
			req_['transferred_ack']= smart_str(req.response.legal_sig)
			req_['transferred_rereq']= smart_str(req.response.legal_tra)
			req_['payment']= smart_str(req.response.legal_cost)
			req_['dissatisfaction_reason'] = smart_str([dr for dr in req.response.dissatisfaction_reason.all()])
			req_['legal_pursue'] = smart_str(req.response.legal_pursue)
		except Exception as e:
			print e
			req_['has_response'] = False
		ta = []
		for a in arr:
			ta.append(req_.get(a))
		writer.writerow(ta)
	return response