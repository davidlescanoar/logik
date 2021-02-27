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

#Devuelve lista de problemas que submiteó determinado usuario en Codeforces
def submissions_codeforces(user_handle, count=20):
    #Intentamos hacer la query
    try:
        #URL de la API de Codeforces
        url = "https://codeforces.com/api/user.status?handle={}&count={}".format(user_handle, count)
        response = requests.request("GET", url, headers={}, data = {}, timeout=5)
        return response.json()
    except BaseException as e:
        raise ValueError("Funcion API: submissions_codeforces. Error: {}".format(str(e)))


def update_Codeforces(user, database, request_cf):
    if not(request_cf and str(request_cf)!='ERROR' and request_cf['status'] and request_cf['status']=='OK'):
        raise ValueError("Error al llamar a API de Codeforces")

    #Guardo solo los envios correctos
    envios = [s for s in request_cf['result'] if 'contestId' in s['problem'] and s['verdict']=='OK']
    problemas = database.objects.filter(judge = 'Codeforces')
    validos = [p for p in problemas for s in envios if p.problem_link.split("problem/")[1] == str(s['problem']['contestId'])+'/'+s['problem']['index']]
    
    for p in validos:
        solved_by=json.loads(p.solvedBy) # Convierto a dict
        try: 
            solved_by[str(user)]=p.problem_points # Actualizo score
        except:
            solved_by[str(user)]=100 # Actualizo score
        database.objects.filter(problem_link=p.problem_link).update(solvedBy=json.dumps(solved_by)) # Hago el update en la DB


@shared_task
def validarCuentaCodeforces(CF_Handle_Input, UserID, Logik_Handle, timeInit):
    if len(str(CF_Handle_Input)) < 1:
        return "Campo CF_Handle_Input vacio"

    request_cf = submissions_codeforces(CF_Handle_Input)

    if not(request_cf and str(request_cf)!='ERROR' and request_cf['status'] and request_cf['status']=='OK'):
        raise ValueError("Error al llamar a API de Codeforces")
    
    try:
        for s in request_cf['result']:
            if(s['problem']['contestId'] == 38 and s['problem']['index'] == "A" and s['verdict'] == "COMPILATION_ERROR"):
                if(timeInit <= s['creationTimeSeconds'] <= timeInit+360):
                    #Si UserID existía en la DB, actualizo el handle de codeforces
                    if Account.objects.filter(AccountID=UserID).exists():
                        Account.objects.filter(AccountID=UserID).update(CF_Handle=CF_Handle_Input)
                    else: #Si no existía en la DB, lo inserto
                        Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle=CF_Handle_Input, OIAJ_Handle='', CSES_Handle='', SPOJ_Handle='', OnlineJudge_Handle='')

                    print("Usuario {} asoció su handle de codeforces: {}".format(Logik_Handle, CF_Handle_Input))
                    request_cf2 = submissions_codeforces(CF_Handle_Input, count=2000000)
                    update_Codeforces(Logik_Handle, Problems, request_cf2)
                    update_Codeforces(Logik_Handle, recommended, request_cf2)
                    print("Usuario {} actualizo correctamente todos los submissions de codeforces: {}".format(Logik_Handle, CF_Handle_Input))
                    
                    return
    except BaseException as e:
        raise ValueError("Error al asociar cuenta de codeforces: {}".format(str(e)))