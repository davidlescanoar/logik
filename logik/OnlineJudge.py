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

def submissions_OnlineJudge(OnlineJudge_ID):
    try:
        OnlineJudge_URL = 'https://uhunt.onlinejudge.org/api/subs-user/'+str(OnlineJudge_ID)
        response = requests.request("GET", OnlineJudge_URL, headers = {}, data = {}, timeout=2).json()
        accepted = dict((x[1], 100) for x in response['subs'] if int(x[2])==90)
        failed = dict((x[1], 0) for x in response['subs'] if int(x[2])!=90 and int(x[1]) not in accepted)
        return {**accepted, **failed}
    except BaseException as e:
        raise ValueError("Funcion API: submissions_OnlineJudge. Error: {}".format(str(e)))


def update_OnlineJudge(user, database, envios):
    if not envios:
        raise ValueError("Error al llamar a API de OnlineJudge")

    problemas = database.objects.filter(judge = 'OnlineJudge')
    validos = [(p, envios[r]) for p in problemas for r in envios if int(p.problem_link[p.problem_link.rindex('=')+1::]) == r]
    
    for p in validos:
        solved_by = json.loads(p[0].solvedBy) # Convierto a dict
        solved_by[str(user)] = p[1] # Actualizo score
        database.objects.filter(problem_link=p[0].problem_link).update(solvedBy=json.dumps(solved_by)) # Hago el update en la DB


#Actualizar cuenta de OnlineJudge
@shared_task
def actualizarCuentaOnlineJudge(OnlineJudge_Handle_Input, UserID, Logik_Handle, fNow):
    if len(str(OnlineJudge_Handle_Input)) < 1:
        return "Campo OnlineJudge_Handle_Input vacio"

    try:
        if Account.objects.filter(AccountID=UserID).exists():
            Account.objects.filter(AccountID=UserID).update(OnlineJudge_Handle=OnlineJudge_Handle_Input)
        #Si no existía en la DB, lo inserto
        else:
            Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle='', OIAJ_Handle='', CSES_Handle='', SPOJ_Handle='',  OnlineJudge_Handle=OnlineJudge_Handle_Input)

        print("Usuario {} asoció su handle de OnlineJudge: {}".format(Logik_Handle, OnlineJudge_Handle_Input))
        request_OnlineJudge = submissions_OnlineJudge(OnlineJudge_Handle_Input)
        update_OnlineJudge(Logik_Handle, Problems, request_OnlineJudge)
        update_OnlineJudge(Logik_Handle, recommended, request_OnlineJudge)
        print("Usuario {} actualizo correctamente todos los submissions de OnlineJudge: {}".format(Logik_Handle, OnlineJudge_Handle_Input))
    except BaseException as e:
        raise ValueError("Error al asociar cuenta de OnlineJudge: {}".format(str(e)))
