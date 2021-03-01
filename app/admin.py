from django.contrib import admin
from app.models import Account, BlackList, Problems, Recommended, Tutorial


class AdminAccount(admin.ModelAdmin):
    list_display = (
    'AccountID', 'Logik_Handle', 'CF_Handle', 'OIAJ_Handle', 'CSES_Handle', 'SPOJ_Handle', 'OnlineJudge_Handle')


class AdminBlackList(admin.ModelAdmin):
    list_display = ('black_user',)


class Problem(admin.ModelAdmin):
    list_display = ('judge', 'problem_link', 'problem_name', 'problem_points', 'solvedBy')


class AdminRecommended(admin.ModelAdmin):
    list_display = ('judge', 'problem_name', 'problem_link', 'solvedBy')


class TutorialAdmin(admin.ModelAdmin):
    list_display = ('id_tutorial', 'titulo', 'autor')


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Recommended, AdminRecommended)
admin.site.register(Problems, Problem)
admin.site.register(Account, AdminAccount)
admin.site.register(BlackList, AdminBlackList)
