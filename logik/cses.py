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

#Actualizar cuenta de CSES
@shared_task
def actualizarCuentaCSES(CSES_Handle_Input, UserID, Logik_Handle, fNow):
    if len(str(CSES_Handle_Input)) < 1:
        return "Campo CSES_Handle_Input vacio"

    try:
        if Account.objects.filter(AccountID=UserID).exists():
            Account.objects.filter(AccountID=UserID).update(CSES_Handle=CSES_Handle_Input)
        #Si no existía en la DB, lo inserto
        else:
            Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle='', OIAJ_Handle='', CSES_Handle=CSES_Handle_Input)
        print("Usuario {} asoció su handle de CSES: {}".format(Logik_Handle, CSES_Handle_Input))
    except BaseException as e:
        raise ValueError("Error al asociar cuenta de CSES: {}".format(str(e)))

def submissions_CSES(CSES_ID):
    try:
        CSES_URL = 'https://cses.fi/problemset/user/'+str(CSES_ID)+'/'
        response = requests.request("GET", CSES_URL, headers = {'Cookie': 'PHPSESSID=83dd884e97206f2e4bb806a8b47ca29a301de0ed'}, data = {}, timeout=2)
        soup = BeautifulSoup(response.content, "html.parser")
        accepted = dict(('https://cses.fi'+x["href"], 100) for x in soup.findAll("a", attrs = {"class" : "full"}))
        return accepted
    except BaseException as e:
        raise ValueError("Funcion API: submissions_CSES. Error: {}".format(str(e)))

def update_CSES(user, database, envios):
    if not envios:
        raise ValueError("Error al llamar a API de CSES")

    problemas = database.objects.filter(judge = 'CSES')
    validos = [(p, envios[r]) for p in problemas for r in envios if p.problem_link == r]
    
    for p in validos:
        solved_by = json.loads(p[0].solvedBy) # Convierto a dict
        solved_by[str(user)] = p[1] # Actualizo score
        database.objects.filter(problem_link=p[0].problem_link).update(solvedBy=json.dumps(solved_by)) # Hago el update en la DB
