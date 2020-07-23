from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery  
from celery.schedules import crontab
from time import sleep
from accounts.models import Account
import users
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime 
from datetime import timedelta
import json
from datetime import timedelta
from logik.celery import app
from django.contrib.auth.models import User
from problems.models import Problems
from recommended.models import recommended
from logik.oiaj import *
from logik.codeforces import *
from logik.cses import *

def vaciarSolvedBy():
    for p in Problems.objects.all():
        Problems.objects.filter(problem_link=p.problem_link).update(solvedBy="{}") # Hago el update en la DB
    
    for p in recommended.objects.all():
        recommended.objects.filter(problem_link=p.problem_link).update(solvedBy="{}") # Hago el update en la DB
    
#Periodic-task
@shared_task
def update_ranking():
    #Usuarios
    users=User.objects.all()

    for user in users:
        cuenta=Account.objects.filter(Logik_Handle=user)
        if  cuenta.exists():
            #Update OIAJ
            if cuenta[0].OIAJ_Handle:
                print("Llamando a la funcion update_OIAJ para user {} ({})".format(cuenta[0].OIAJ_Handle, user))
                try:
                    request_oiaj = submissions_OIAJ(cuenta[0].OIAJ_Handle)
                    try:
                        update_OIAJ(user, Problems, request_oiaj)
                        update_OIAJ(user, recommended, request_oiaj)
                    except BaseException as e:
                        print("Error con el usuario {} ({}) al llamar update_OIAJ. Error: {}".format(cuenta[0].OIAJ_Handle, user, str(e)))
                except BaseException as e:
                    print("Error en update_ranking: {}".format(str(e)))


            #Update Codeforces
            if cuenta[0].CF_Handle:
                print("Llamando a la funcion update_Codeforces para user {} ({})".format(cuenta[0].CF_Handle, user))
                try:
                    request_cf = submissions_codeforces(cuenta[0].CF_Handle)
                    try:
                        update_Codeforces(user, Problems, request_cf)
                        update_Codeforces(user, recommended, request_cf)
                    except BaseException as e:
                        print("Error con el usuario {} ({}) al llamar update_Codeforces. Error: {}".format(cuenta[0].CF_Handle, user, str(e)))               
                except BaseException as e:
                    print("Error en update_ranking: {}".format(str(e)))

                    
            #Update CSES
            if cuenta[0].CSES_Handle:
                print("Llamando a la funcion update_CSES para user {} ({})".format(cuenta[0].CSES_Handle, user))
                try:
                    request_cses = submissions_CSES(cuenta[0].CSES_Handle)
                    try:
                        update_CSES(user, Problems, request_cses)
                        update_CSES(user, recommended, request_cses)
                    except BaseException as e:
                        print("Error con el usuario {} ({}) al llamar update_CSES. Error: {}".format(cuenta[0].CSES_Handle, user, str(e)))               
                except BaseException as e:
                    print("Error en update_ranking: {}".format(str(e)))

"""
Script para testear esta función y medir tiempo

python manage.py shell

from timeit import default_timer as timer
from logik.tasks import update_ranking as f

start = timer()
f.apply()
end = timer()
print(end - start)

"""