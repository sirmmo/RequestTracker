from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import User

class Requester(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=250,verbose_name=_('Name'))
	surname = models.CharField(max_length=250,verbose_name=_('Surname'))
	organization = models.CharField(max_length=250,verbose_name=_('Organization'))
	
	def __str__(self):
		return "%s %s (%s)" % (self.name, self.surname, self.organization, )
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Requester._meta.fields]

class SatisfactionLevel(models.Model):
	level = models.IntegerField()
	
	def __str__(self):
		return str(self.level)
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in SatisfactionLevel._meta.fields]

class DissatisfactionType(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return self.name
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in DissatisfactionType._meta.fields]


class Topic(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return self.name
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Topic._meta.fields]


class Level(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return self.name
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Level._meta.fields]


class Request(models.Model):
	requester = models.ForeignKey(Requester)
	question = models.TextField(verbose_name=_('Request'), help_text=_("You can insert the text fo the request - it will not be exposed - or simply the specific topic of your request"))
	submission_date = models.DateField(verbose_name=_('Submission Date'))
	topic = models.ForeignKey(Topic, verbose_name=_('Topic'))
	level = models.ForeignKey(Level, verbose_name=_('Type'))
	
	def __str__(self):
		return "%s - %s" % (self.requester, self.topic)
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Request._meta.fields if field.name not in ['ID', 'request', 'requester']]

	
class Response(models.Model):
	request = models.OneToOneField(Request, related_name="response")
	response_date = models.DateField(blank=True, null=True)
	satisfaction_level = models.ForeignKey(SatisfactionLevel)
	dissatisfaction_reason = models.ManyToManyField(DissatisfactionType)
	legal_pursue = models.BooleanField(help_text="Saresti disposto a fare denuncia al TAR per ottenere questi dati?")
	legal_support = models.BooleanField(help_text="La tua redazione sarebbe disposta a supportare le spese legali per il ricorso?")

	def __str__(self):
		return "%s => %s" % (self.request, self.satisfaction_level )
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Response._meta.fields if field.name not in ['ID', 'request', 'requester']]

