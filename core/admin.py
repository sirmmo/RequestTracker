from django.db import models
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from core.models import *

from django.contrib import admin




def export_as_csv(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/data.csv")

admin.site.add_action(export_as_csv, 'export')
admin.site.disable_action('export')

class RequestAdmin(admin.ModelAdmin):
    actions = ['export']


admin.site.register(Requester)
admin.site.register(SatisfactionLevel)
admin.site.register(DissatisfactionType)
admin.site.register(Topic)
admin.site.register(Level)
admin.site.register(Request, RequestAdmin)
admin.site.register(Area)
admin.site.register(Response)