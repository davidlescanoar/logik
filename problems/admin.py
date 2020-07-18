from django.contrib import admin
from problems.models import Problems

# Register your models here.
class Problem(admin.ModelAdmin):
    list_display=('judge', 'problem_link', 'problem_name', 'problem_points', 'solvedBy')

admin.site.register(Problems, Problem)