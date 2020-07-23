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

#Devuelve lista de problemas que submiteó determinado usuario en Codeforces
def submissions_codeforces(user_handle):
    #Intentamos hacer la query
    try:
        #URL de la API de Codeforces
        url = 'https://codeforces.com/api/user.status?handle='+user_handle+'&count=20'
        response = requests.request("GET", url, headers={}, data = {}, timeout=10)
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
    request_cf = submissions_codeforces(CF_Handle_Input)

    if not(request_cf and str(request_cf)!='ERROR' and request_cf['status'] and request_cf['status']=='OK'):
        raise ValueError("Error al llamar a API de Codeforces")
    
    for s in request_cf['result']:
        if(s['problem']['contestId'] == 38 and s['problem']['index'] == "A" and s['verdict'] == "COMPILATION_ERROR"):
            if(timeInit <= s['creationTimeSeconds'] <= timeInit+360):
                print("Usuario {} asoció correctamente su handle de codeforces: {}".format(Logik_Handle, CF_Handle_Input))

                #Si UserID existía en la DB, actualizo el handle de codeforces
                if Account.objects.filter(AccountID=UserID).exists():
                    Account.objects.filter(AccountID=UserID).update(CF_Handle=CF_Handle_Input)
                else: #Si no existía en la DB, lo inserto
                    Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle=CF_Handle_Input, OIAJ_Handle='', CSES_Handle='')
                return