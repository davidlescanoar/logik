from django.contrib import admin
from recommended.models import recommended

# Register your models here.
class AdminRecommended(admin.ModelAdmin):
    list_display=('problem_name', 'problem_link', 'solvedBy', 'oiaj')

admin.site.register(recommended, AdminRecommended)