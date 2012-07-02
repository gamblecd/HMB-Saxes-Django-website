import models
from django.contrib import admin
from django.forms.widgets import TextInput, Textarea
from django.db import models as dmodels

class QuoteAdmin(admin.ModelAdmin):
    formfield_overrides = {
        dmodels.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
    }


class Member_PhotoAdmin(admin.ModelAdmin):
        list_display = ['member', 'admin_thumbnail']
        
admin.site.register(models.Member_Photo, Member_PhotoAdmin)
admin.site.register(models.Member)
admin.site.register(models.Quote, QuoteAdmin)
admin.site.register(models.Post)