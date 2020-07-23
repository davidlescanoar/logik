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


#Validar usuario de OIAJ
@shared_task
def validarCuentaOIAJ(OIAJ_Handle_Input, UserID, Logik_Handle, fNow):
    #Url de los submissions del problema a verificar
    url="http://juez.oia.unsam.edu.ar/api/submission"
    #String del error esperado
    problem_error="fail"

    #Convertir fNow a datetime
    fechaNow=datetime.datetime.strptime(fNow, '%Y-%m-%dT%H:%M:%S.%f').replace(second=0, microsecond=0)
    #Fecha limite de submission
    fechaLimite=fechaNow+timedelta(minutes=6)

    #Headers
    headers={
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "es-419,es;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "69",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "_ga=GA1.5.839228822.1582983670; __cfduid=db34d8daa05b7440e2d3eb3a49ef31c7a1590185696; _gid=GA1.5.232300576.1592232757; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRhdmlkbGVzY2FubyIsInBpY3R1cmUiOiIvL2dyYXZhdGFyLmNvbS9hdmF0YXIvODE1ZTI4YTZjY2RhODRiYjlkYzRlODgzZDYxYTcxMDI_ZD1pZGVudGljb24iLCJmaXJzdE5hbWUiOiJEYXZpZCIsImxhc3ROYW1lIjoiTGVzY2FubyIsImVtYWlsIjoiZGF2bGVza2EwOUBnbWFpbC5jb20iLCJpZCI6MTQ0fQ.oZm5lEbQt4VF8LgtHXzqRfBDewmKQlBb7dwWM97Gt4w; cf_ob_info=520:5a3d7af6faaed2d0:EZE; cf_use_ob=80",
        "Host": "juez.oia.unsam.edu.ar",
        "Origin": "http://juez.oia.unsam.edu.ar",
        "Referer": "http://juez.oia.unsam.edu.ar/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"

    }

    #Payload (datos que se le van a pasar a la API)
    payload= {"action":"list","task_name":"es_bisiesto","username":OIAJ_Handle_Input}
    
    #Obtengo los datos
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    #Lo paso a dict
    json_data=json.loads(response.content)

    #Por cada submission
    for i in json_data['submissions']:
        #Resultado de compilación, para validar tiene que tener un error
        resultado_compilacion=i['compilation_outcome']
        #Timestamp del submission
        timestamp=i['timestamp']
        #Pasamos timestamp a datetime
        fechaSubmission=datetime.datetime.strptime(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%f'), '%Y-%m-%dT%H:%M:%S.%f')

        #Si el submission tiene el error esperado y está en la ventana de 6 minutos, significa que se validó con éxito
        if resultado_compilacion==problem_error and fechaNow<=fechaSubmission and fechaSubmission<=fechaLimite:
            #Si UserID existía en la DB, actualizo el handle de OIAJ
            if Account.objects.filter(AccountID=UserID).exists():
                Account.objects.filter(AccountID=UserID).update(OIAJ_Handle=OIAJ_Handle_Input)
            #Si no existía en la DB, lo inserto
            else:
                Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle='', OIAJ_Handle=OIAJ_Handle_Input, CSES_Handle='')


#Devuelve lista de problemas que submiteó determinado usuario en OIAJ
def submissions_OIAJ(user_handle):
    #Url de la API de OIAJ
    url = "http://juez.oia.unsam.edu.ar/api/user"

    #Parámetros
    payload = '{"action": "get", "username": "' + user_handle + '"}'
    headers = {
    'Content-Type': 'application/json',
    'Cookie': '__cfduid=d7719a9f82edfdbfb79cffbe9600b07ff1590280585'
    }

    #Intentamos hacer la query
    try: 
        response = requests.request("POST", url, headers=headers, data = payload, timeout=2)
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
