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
	level = models.TextField()
	
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
		return [(field.verbose_name, str(self.__getattribute__(field.name))) for field in Level._meta.fields]


class Request(models.Model):
	requester = models.ForeignKey(Requester)
	question = models.TextField(verbose_name=_('Request'), help_text=_("You can insert the text fo the request - it will not be exposed - or simply the specific topic of your request"))
	submission_date = models.DateField(verbose_name=_('Submission Date'))
	topic = models.ForeignKey(Topic, verbose_name=_('Topic'))
	level = models.ForeignKey(Level, verbose_name=_('Type'))
	
	def __str__(self):
		return "%s - %s" % (self.requester, self.topic)
	def get_fields(self):
		rl = []
		for field in Request._meta.fields:
			if field.name not in ['id', 'request', 'requester']:
				rl.append((field.verbose_name, str(self.__getattribute__(field.name))))
		return [(field.verbose_name, str(self.__getattribute__(field.name))) for field in Request._meta.fields if field.name not in ['id', 'request', 'requester']]



class Response(models.Model):
	request = models.OneToOneField(Request, related_name="response")
	response_date = models.DateField(verbose_name=_('Response Date'), blank=True, null=True)
	satisfaction_level = models.ForeignKey(SatisfactionLevel, verbose_name=_("Come consideri la qualita' della risposta?"),blank=True, null=True)

	dissatisfaction_reason = models.ManyToManyField(DissatisfactionType,verbose_name=_("L'informazione che hai chiesto non ti e' stata data? Perche'?"),blank=True, null=True)
	legal_pursue = models.NullBooleanField(verbose_name=_("In caso di risposta negativa da parte della PA vorresti fare ricorso per ottenere l'accesso alle informazioni che hai richiesto?"),blank=True, null=True)
	legal_support = models.NullBooleanField(verbose_name=_("Hai avuto supporto legale per fare questa richiesta?"),blank=True, null=True)
	
	legal_ack = models.NullBooleanField(verbose_name=_("Hai ricevuto dal destinatario della richiesta una segnalazione dell'avvenuta richiesta e ricezione della stessa?"),blank=True, null=True)
	legal_ent = models.NullBooleanField(verbose_name=_("La richiesta e' stata trasferita ad altra ufficio/ente?"),blank=True, null=True)
	legal_sig = models.NullBooleanField(verbose_name=_("Il trasferimento ti e' stato segnalato?"),blank=True, null=True)
	legal_tra = models.NullBooleanField(verbose_name=_("In seguito al trasferimento devi rifare la richiesta?"),blank=True, null=True)
	legal_cost = models.NullBooleanField(verbose_name=_("Hai ricevuto una richiesta di pagamento superiore ai costi di copia e spedizione?"),blank=True, null=True)

	def __str__(self):
		return "%s => %s" % (self.request, self.satisfaction_level )
	def get_fields(self):
		return [(field.verbose_name, str(self.__getattribute__(field.name))) for field in Response._meta.fields if field.name not in ['id', 'request', 'requester']]

