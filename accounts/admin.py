from django.contrib import admin
from accounts.models import Account

# Register your models here.

class AdminAccount(admin.ModelAdmin):
    list_display=('AccountID', 'Logik_Handle', 'CF_Handle', 'OIAJ_Handle')

admin.site.register(Account, AdminAccount)