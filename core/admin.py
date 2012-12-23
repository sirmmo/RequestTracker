from django.db import models
from django.contrib.auth.models import User

from core.models import *

from django.contrib.admin import site

site.register(Requester)
site.register(SatisfactionLevel)
site.register(DisSatisfactionType)
site.register(Area)
site.register(Level)
site.register(Request)
site.register(Response)
