from django.contrib import admin
from tutorial.models import Tutorial

# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    list_display=('id_tutorial','titulo','autor')

admin.site.register(Tutorial,TutorialAdmin)