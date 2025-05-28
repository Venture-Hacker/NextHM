from django.contrib import admin
from core.models import *
# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','submitted_at')
    search_fields = ('name', 'email')

admin.site.register(Feedback, FeedbackAdmin)