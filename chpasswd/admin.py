from django.contrib import admin
from models import (
    ADUser,
    PasswordChangeLog,
)


class ADUserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = ('username',)
    readonly_fields = ('username',)


class PasswordChangeLogAdmin(admin.ModelAdmin):
    search_fields = ('ad_user__username', 'source_ip')
    list_display = ('ad_user', 'source_ip', 'when', 'success')
    list_filter = ('success', )
    ordering = ('when', )
    readonly_fields = (
        'ad_user', 'source_ip', 'when', 'success', 'fail_reason')


admin.site.register(ADUser, ADUserAdmin)
admin.site.register(PasswordChangeLog, PasswordChangeLogAdmin)
