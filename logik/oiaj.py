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

#Devuelve lista de problemas que submiteó determinado usuario en OIAJ
def submissions_OIAJ(user_handle):
    url = "http://juez.oia.unsam.edu.ar/api/user"
    payload = {"action":"get", "username": user_handle}
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    #Intentamos hacer la query
    try: 
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), timeout=2)
        return response.json()
    except BaseException as e:
        raise ValueError("Funcion API: submissions_OIAJ. Error: {}".format(str(e)))


def update_OIAJ(user, database, request_oiaj):
    if not(request_oiaj and 'scores' in request_oiaj):
        raise ValueError("Error al llamar a API de OIAJ")

    envios = request_oiaj['scores']
    problemas = database.objects.filter(judge = 'OIAJ')
    validos = [(p, r['score']) for p in problemas for r in envios if p.problem_link.split('/')[5] == r['name']]
    
    for p in validos:
        solved_by = json.loads(p[0].solvedBy) # Convierto a dict
        solved_by[str(user)] = p[1] # Actualizo score
        database.objects.filter(problem_link=p[0].problem_link).update(solvedBy=json.dumps(solved_by)) # Hago el update en la DB


#Validar usuario de OIAJ
@shared_task
def validarCuentaOIAJ(OIAJ_Handle_Input, UserID, Logik_Handle, timeInicio):
    if len(str(OIAJ_Handle_Input)) < 1:
        return "Campo OIAJ_Handle_Input vacio"

    try:
        url = "http://juez.oia.unsam.edu.ar/api/submission"
        payload= {"action":"list","task_name":"es_bisiesto","username":OIAJ_Handle_Input}
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        #Obtengo los datos
        response = requests.request("POST", url, headers=headers, data = json.dumps(payload), timeout=2)
        envios = response.json()['submissions']
    except BaseException as e:
        raise ValueError("Funcion API: validarCuentaOIAJ. Error: {}".format(str(e)))

    try:
        for s in envios:
            if(s['compilation_outcome'] == "fail" and timeInicio <= s['timestamp'] <= timeInicio+360):
                #Si UserID existía en la DB, actualizo el handle de OIAJ
                if Account.objects.filter(AccountID=UserID).exists():
                    Account.objects.filter(AccountID=UserID).update(OIAJ_Handle=OIAJ_Handle_Input)
                #Si no existía en la DB, lo inserto
                else:
                    Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, OIAJ_Handle=OIAJ_Handle_Input)
                
                print("Usuario {} asoció su handle de OIAJ: {}".format(Logik_Handle, OIAJ_Handle_Input))
                request_oiaj = submissions_OIAJ(OIAJ_Handle_Input)
                update_OIAJ(Logik_Handle, Problems, request_oiaj)
                update_OIAJ(Logik_Handle, Recommended, request_oiaj)
                print("Usuario {} actualizo correctamente todos los submissions de OIAJ: {}".format(Logik_Handle, OIAJ_Handle_Input))
                return
    except BaseException as e:
        raise ValueError("Error al asociar cuenta de OIAJ: {}".format(str(e)))