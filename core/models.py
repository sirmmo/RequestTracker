from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str

class Requester(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=250,verbose_name=_('Name'))
	surname = models.CharField(max_length=250,verbose_name=_('Surname'))
	organization = models.CharField(max_length=250,verbose_name=_('Organization'))

	security_question = models.CharField(max_length=500, verbose_name=_("Security Question"))
	security_answer = models.CharField(max_length=500, verbose_name=_("Security Answer"))
	
	def __str__(self):
		return smart_str("%s %s (%s)" % (self.name, self.surname, self.organization, ))
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Requester._meta.fields]

class SatisfactionLevel(models.Model):
	level = models.TextField()
	
	def __str__(self):
		return smart_str(self.level)
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in SatisfactionLevel._meta.fields]

class DissatisfactionType(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return smart_str(self.name)
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in DissatisfactionType._meta.fields]


class Topic(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return smart_str(self.name)
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Topic._meta.fields]


class Area(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return smart_str(self.name)
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Area._meta.fields]


class Level(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return smart_str(self.name)
	def get_fields(self):
		return [(field.verbose_name, str(self.__getattribute__(field.name))) for field in Level._meta.fields]


vowel = "aeiou"
def get_consonants(string):
	res = ""
	for c in string:
		if c not in vowel:
			res += c
	return res

class Request(models.Model):
	code = models.CharField(max_length=100, blank=True, null=True)
	requester = models.ForeignKey(Requester)
	question = models.TextField(verbose_name=_('Request'), help_text=_("You can insert the text fo the request - it will not be exposed - or simply the specific topic of your request"))
	submission_date = models.DateField(verbose_name=_('Submission Date'))
	#yes, this sucks, but it works "in progress".
	topic = models.ForeignKey(Area, verbose_name=_('Topic'))
	area = models.ForeignKey(Topic, verbose_name=_('Area'))
	level = models.ForeignKey(Level, verbose_name=_('Type'))
	
	def __str__(self):
		return smart_str("%s - %s" % (self.requester, self.topic))
	def get_fields(self):
		rl = []
		'''for field in Request._meta.fields:
			if field.name not in ['id', 'request', 'requester']:
				rl.append((field.verbose_name, smart_str(self.__getattribute__(field.name))))'''
		return [(field.verbose_name, unicode(self.__getattribute__(field.name))) for field in Request._meta.fields if field.name not in ['id', 'request', 'requester']]
	def save(self, *args, **kwargs):
		if self.code is  None:
			self.code = get_consonants(self.requester.name.lower())[:2].upper() + get_consonants(self.requester.surname.lower())[:2].upper() + self.submission_date.strftime('%d%m')+ "-"+str(Request.objects.filter(requester = self.requester, submission_date__day = self.submission_date.day).count()+1)
		super(Request, self).save(*args, **kwargs)


def get_no_satis():
	return SatisfactionLevel.objects.get(id=6)

class Response(models.Model):
	request = models.OneToOneField(Request, related_name="response")
	response_date = models.DateField(verbose_name=_('Response Date'), blank=True, null=True)
	satisfaction_level = models.ForeignKey(SatisfactionLevel, verbose_name=_("Come consideri la qualita' della risposta?"), default=get_no_satis, null=False, blank=False)

	dissatisfaction_reason = models.ManyToManyField(DissatisfactionType,verbose_name=_("L'informazione che hai chiesto non ti e' stata data. Perche'?"),blank=True, null=True)
	legal_pursue = models.NullBooleanField(verbose_name=_("In caso di risposta negativa da parte della PA vorresti fare ricorso per ottenere l'accesso alle informazioni che hai richiesto?"),blank=True, null=True)
	legal_support = models.NullBooleanField(verbose_name=_("Hai avuto supporto legale per fare questa richiesta?"),blank=True, null=True)
	
	legal_ack = models.NullBooleanField(verbose_name=_("Hai ricevuto dal destinatario della richiesta una segnalazione dell'avvenuta richiesta e ricezione della stessa?"),blank=True, null=True)
	legal_ent = models.NullBooleanField(verbose_name=_("La richiesta e' stata trasferita ad altra ufficio/ente?"),blank=True, null=True)
	legal_sig = models.NullBooleanField(verbose_name=_("Il trasferimento ti e' stato segnalato?"),blank=True, null=True)
	legal_tra = models.NullBooleanField(verbose_name=_("In seguito al trasferimento hai dovuto rifare la richiesta?"),blank=True, null=True)
	legal_cost = models.NullBooleanField(verbose_name=_("Hai ricevuto una richiesta di pagamento superiore ai costi di copia e spedizione?"),blank=True, null=True)

	def __str__(self):
		return smart_str("%s - %s" % (self.request, self.response_date ))
	def get_fields(self):
		rl = []
		for field in Response._meta.fields:
			if field.name not in ['id', 'request', 'requester']:
				rl.append((field.verbose_name, str(self.__getattribute__(field.name))))
		return [(field.verbose_name, _(str(self.__getattribute__(field.name)))) for field in Response._meta.fields if field.name not in ['id', 'request', 'requester']]


