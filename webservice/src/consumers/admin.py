from django.contrib import admin
from consumers.models import Consumer


class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'created', 'updated', 'is_valid')
    ordering = ('created',)

admin.site.register(Consumer, ConsumerAdmin)
