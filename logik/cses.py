from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery  
from celery.schedules import crontab
from time import sleep
from app.models import *
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

def submissions_CSES(CSES_ID):
    try:
        CSES_URL = 'https://cses.fi/problemset/user/'+str(CSES_ID)+'/'
        response = requests.request("GET", CSES_URL, headers = {'Cookie': 'PHPSESSID=83dd884e97206f2e4bb806a8b47ca29a301de0ed'}, data = {}, timeout=2)
        soup = BeautifulSoup(response.content, "html.parser")
        accepted = dict(('https://cses.fi'+x["href"], 100) for x in soup.findAll("a", attrs = {"class" : "full"}))
        failed = dict(('https://cses.fi'+x["href"], 0) for x in soup.findAll("a", attrs = {"class" : "zero"}))
        return {**accepted, **failed}
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
            Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle='', OIAJ_Handle='', CSES_Handle=CSES_Handle_Input, SPOJ_Handle='', OnlineJudge_Handle='')

        print("Usuario {} asoció su handle de CSES: {}".format(Logik_Handle, CSES_Handle_Input))
        request_cses = submissions_CSES(CSES_Handle_Input)
        update_CSES(Logik_Handle, Problems, request_cses)
        update_CSES(Logik_Handle, recommended, request_cses)
        print("Usuario {} actualizo correctamente todos los submissions de CSES: {}".format(Logik_Handle, CSES_Handle_Input))
    except BaseException as e:
        raise ValueError("Error al asociar cuenta de CSES: {}".format(str(e)))
