from django.contrib import admin

from .models import PastedData
# Register your models here.

class PastedAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['title']}),
        ('Article',{'fields': ['article']}),
        ('Date information', {'fields': ['first_pasted'],}),
    ]
    list_display = ('title', 'type', 'count')
    list_filter = ['type']

admin.site.register(PastedData, PastedAdmin)

