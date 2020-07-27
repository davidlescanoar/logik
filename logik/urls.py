"""logik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import welcome, login, logout, register
from accounts.views import accounts
from problems.views import problems
from ranking.views import ranking
from recommended.views import recommended
from contest.views import contest, contestManager, editContest, createContest
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('accounts/', accounts),
    path('problems/', problems),
    path('ranking/', ranking),
    path('recommended/', recommended),
    path('contests/', contest),
    path('contestManager/', contestManager),
    path('editContest/', editContest),
    path('createContest/', createContest),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
