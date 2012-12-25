from django.db import models
from django.contrib.auth.models import User

class Requester(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=250)
	surname = models.CharField(max_length=250)
	organization = models.CharField(max_length=250)
	
	def __str__(self):
		return "%s %s (%s)" % (self.name, self.surname, self.organization, )

class SatisfactionLevel(models.Model):
	level = models.IntegerField()
	
	def __str__(self):
		return str(self.level)

class DissatisfactionType(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return self.name

class Topic(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return self.name

class Level(models.Model):
	name = models.TextField()
	
	def __str__(self):
		return self.name

class Request(models.Model):
	requester = models.ForeignKey(Requester)
	question = models.TextField()
	submission_date = models.DateField()
	topic = models.ForeignKey(Topic)
	level = models.ForeignKey(Level)
	
	def __str__(self):
		return "%s - %s" % (self.requester, self.topic)
	
class Response(models.Model):
	request = models.OneToOneField(Request, related_name="response")
	response_date = models.DateField(blank=True, null=True)
	satisfaction_level = models.ForeignKey(SatisfactionLevel)
	dissatisfaction_reason = models.ManyToManyField(DissatisfactionType)
	legal_pursue = models.BooleanField(help_text="Saresti disposto a fare denuncia al TAR per ottenere questi dati?")
	legal_support = models.BooleanField(help_text="La tua redazione sarebbe disposta a supportare le spese legali per il ricorso?")

	def __str__(self):
		return "%s => %s" % (self.request, self.satisfaction)