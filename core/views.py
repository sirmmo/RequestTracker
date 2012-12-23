from django.forms import ModelForm
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
import json
from core.models import *

def index (request):
	return render_to_response('index.html', {'know_user':False})

class RequestForm(ModelForm):
	class Meta:
		model = Request
		exclude = ('requester')

class ResponseForm(ModelForm):
	class Meta:
		model = Response
		
@login_required
def profile(request):
	pass

class RequestListView(ListView):
    model = Request
    template_name = "requests.html"
    
class RequestCreate(CreateView):
	model = Request
	exclude = ('requester')
	template_name = "form.html"

class RequestUpdate(UpdateView):
	model = Request
	exclude = ('requester')
	template_name = "form.html"

class RequestDelete(DeleteView):
    model = Request

class RequestView(FormView):
	form_class = RequestForm
	model = Request
	template_name = "form.html"
	def form_valid(self, form):
		form.instance.requester.user = self.request.user
		return super(RequestForm, self).form_valid(form)

class ResponseView(FormView):
        form_class = ResponseForm
	model = Response
	template_name = "form.html"
        def form_valid(self, form):
                return super(ResponseForm, self).form_valid(form)


def req_stats(request):
	r = []
	for req in Request.objects.all():
		req_ = {}
		req_['user'] = str(req.requester)
		req_['organization'] = str(req.requester.organization)
		req_['submission_date'] = str(req.submission_date)
		req_['area'] = str(req.area)
		req_['level'] = str(req.level)
		try:
			t = req.response
			req_['has_response'] = True
			req_['satisfaction']= str(req.response.satisfaction)
			req_['response_date'] = str(req.response.answer_date)
		except:
			req_['has_response'] = False
		r.append(req_)

	return HttpResponse(json.dumps(r))
