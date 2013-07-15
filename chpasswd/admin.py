from django.contrib import admin
from models import (
    ADUser,
    PasswordChangeLog,
)

admin.site.register(ADUser)
admin.site.register(PasswordChangeLog)

