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

#Validar usuario de codeforces
@shared_task
def validarCuentaCodeforces(CF_Handle_Input, UserID, Logik_Handle, fNow):
    #Url de los submissions, nombre de problema a submitear y error esperado respectivamente
    url="https://codeforces.com/submissions/"+CF_Handle_Input
    CF_Problem_Name="A - Army"
    CF_Error_Name="Compilation error"

    #Convertir fNow a datetime
    fechaNow=datetime.datetime.strptime(fNow, '%Y-%m-%dT%H:%M:%S.%f').replace(second=0, microsecond=0)
    #Fecha limite de submission
    fechaLimite=fechaNow+timedelta(minutes=6)

    #Obtengo el html
    response = requests.get(url)

    #Lo formateo
    soup = BeautifulSoup(response.text, "html.parser")

    #Encuentro todas las etiquetas tr
    submissions=soup.findAll("tr")

    #Por cada "submission"
    for i in submissions:
        #Lo casteo
        submission=i.prettify()

        #Si el submission contiene el handle del usuario, es del problema que se especificó en la variable CF_Problem_Name y tiene el error esperado
        #se verifica si la fecha está en el intervalo deseado
        if CF_Handle_Input in submission and CF_Problem_Name in submission and CF_Error_Name in submission:
            tds=0

            #Recorro el string del submission hasta encontrar 2 td (sé que el 2do es el de la fecha, que es el dato que me falta obtener)
            for j in range(len(submission)-2):
                if submission[j:j+3]=="<td":
                    tds+=1

                #Si encontré el 2do td salgo del for, guardandome en qué posición lo encontré
                if tds==2:
                    tds=j
                    break
            
            #Si encontré algún td tengo que darle formato a la fecha
            if tds>0:
                #En fechaUser se va a guardar la fecha en formato string
                fechaUser=""

                cntGreater=0
#TEST COMIT CAMBIO
                #Tengo que avanzar la variable tds hasta que haya pasado dos '>' porque luego del td viene un <span> que no me interesa
                #luego de esas dos cosas viene la fecha
                while  tds<len(submission) and cntGreater<2:
                    if submission[tds]=='>':
                        cntGreater+=1
                    tds+=1

                #Voy agregando los caracteres de la fecha al string fechaUser, hasta que encuentre un '<', que significa que no tengo que leer más
                while tds<len(submission) and submission[tds]!='<':
                    fechaUser+=submission[tds]
                    tds+=1

                #Fecha y hora del submission
                fechaSubmission=datetime.datetime.strptime(fechaUser[4:-3], '%b/%d/%Y %H:%M')-timedelta(hours=3)

                #Si el submission está en la ventana de 6 minutos, significa que se validó con éxito
                if fechaNow<=fechaSubmission and fechaSubmission<=fechaLimite:
                    #Si UserID existía en la DB, actualizo el handle de codeforces
                    if Account.objects.filter(AccountID=UserID).exists():
                        Account.objects.filter(AccountID=UserID).update(CF_Handle=CF_Handle_Input)
                    #Si no existía en la DB, lo inserto
                    else:
                        Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle=CF_Handle_Input, OIAJ_Handle='', CSES_Handle='')

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

#Actualizar cuenta de CSES
@shared_task
def actualizarCuentaCSES(CSES_Handle_Input, UserID, Logik_Handle, fNow):
    #Si UserID existía en la DB, actualizo el handle de OIAJ
    if Account.objects.filter(AccountID=UserID).exists():
        Account.objects.filter(AccountID=UserID).update(CSES_Handle=CSES_Handle_Input)
    #Si no existía en la DB, lo inserto
    else:
        Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle='', OIAJ_Handle='', CSES_Handle=CSES_Handle_Input)

#Devuelve lista de problemas que submiteó determinado usuario en OIAJ
def submissions_OIAJ(user_handle):
    #Url de la API de OIAJ
    url = "http://juez.oia.unsam.edu.ar/api/user"

    #Parámetros
    payload = '{\n    \"action\": \"get\",\n    \"username\":\"'+user_handle+'\"\n}'
    headers = {
    'Content-Type': 'application/json',
    'Cookie': '__cfduid=d7719a9f82edfdbfb79cffbe9600b07ff1590280585'
    }

    #Intentamos hacer la query
    try: 
        response = requests.request("POST", url, headers=headers, data = payload, timeout=2)
        #Devuelvo en JSON
        return response.json()
    except BaseException as e:
        raise ValueError("Funcion API: submissions_OIAJ. Error: {}".format(str(e)))

#Devuelve lista de problemas que submiteó determinado usuario en Codeforces
def submissions_codeforces(user_handle):
    #URL de la API de Codeforces
    url = 'https://codeforces.com/api/user.status?handle='+user_handle+'&count=20'

    #Intentamos hacer la query
    try:
        response = requests.request("GET", url, headers={}, data = {}, timeout=5)
        #Se devuelve el JSON
        return response.json()
    except BaseException as e:
        raise ValueError("Funcion API: submissions_codeforces. Error: {}".format(str(e)))

def submissions_CSES(CSES_ID):
    try:
        CSES_URL = 'https://cses.fi/problemset/user/'+str(CSES_ID)+'/'
        response = requests.request("GET", CSES_URL, headers = {'Cookie': 'PHPSESSID=83dd884e97206f2e4bb806a8b47ca29a301de0ed'}, data = {}, timeout=2)
        soup = BeautifulSoup(response.content, "html.parser")
        accepted = dict(('https://cses.fi'+x["href"], 100) for x in soup.findAll("a", attrs = {"class" : "full"}))
        return accepted
        
    except BaseException as e:
        raise ValueError("Funcion API: submissions_CSES. Error: {}".format(str(e)))

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

def update_CSES(user, database, envios):
    if not envios:
        raise ValueError("Error al llamar a API de CSES")

    problemas = database.objects.filter(judge = 'CSES')
    validos = [(p, envios[r]) for p in problemas for r in envios if p.problem_link == r]
    
    for p in validos:
        solved_by = json.loads(p[0].solvedBy) # Convierto a dict
        solved_by[str(user)] = p[1] # Actualizo score
        database.objects.filter(problem_link=p[0].problem_link).update(solvedBy=json.dumps(solved_by)) # Hago el update en la DB

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

    vaciarSolvedBy()
    return 1

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
                        print('Fallo aca: ' + str(e))
                        print("Error? Con el usuario {} ({}) al llamar update_OIAJ".format(cuenta[0].OIAJ_Handle, user))
                except BaseException as e:
                    print('Fallo aca: ' + str(e))
            #Update Codeforces
            if cuenta[0].CF_Handle:
                print("Llamando a la funcion update_Codeforces para user {} ({})".format(cuenta[0].CF_Handle, user))
                try:
                    request_cf = submissions_codeforces(cuenta[0].CF_Handle)
                    try:
                        update_Codeforces(user, Problems, request_cf)
                        update_Codeforces(user, recommended, request_cf)
                    except BaseException as e:
                        print('Fallo aca: ' + str(e))
                        print("Error? Con el usuario {} ({}) al llamar update_Codeforces".format(cuenta[0].CF_Handle, user))               
                except BaseException as e:
                    print('Fallo aca: ' + str(e))
            #Update CSES
            if cuenta[0].CSES_Handle:
                print("Llamando a la funcion update_CSES para user {} ({})".format(cuenta[0].CSES_Handle, user))
                try:
                    request_cses = submissions_CSES(cuenta[0].CSES_Handle)
                    try:
                        update_CSES(user, Problems, request_cses)
                        update_CSES(user, recommended, request_cses)
                    except BaseException as e:
                        print('Fallo aca: ' + str(e))
                        print("Error? Con el usuario {} ({}) al llamar update_CSES".format(cuenta[0].CSES_Handle, user))               
                except BaseException as e:
                    print('Fallo aca: ' + str(e))

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