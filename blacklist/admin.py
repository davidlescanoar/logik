from django.contrib import admin
from blacklist.models import BlackList

# Register your models here.
class AdminBlackList(admin.ModelAdmin):
    list_display=('black_user',)

admin.site.register(BlackList, AdminBlackList)