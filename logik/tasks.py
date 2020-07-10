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
                        Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle=CF_Handle_Input, OIAJ_Handle='')

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
                Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, CF_Handle='', OIAJ_Handle=OIAJ_Handle_Input)

#Devuelve lista de problemas que submiteó determinado usuario en OIAJ
def submissions_by_user(user_handle):
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
        response = requests.request("POST", url, headers=headers, data = payload, timeout=1)

        #Devuelvo en JSON
        if response:
            return response.json()
    except requests.exceptions.Timeout as err: 
        return "ERROR"

#Devuelve lista de problemas que submiteó determinado usuario en Codeforces
def submissions_codeforces(user_handle):
    #URL de la API de Codeforces
    url = 'https://codeforces.com/api/user.status?handle='+user_handle+'&count=20'

    #Intentamos hacer la query
    try:
        response = requests.request("GET", url, headers={}, data = {}, timeout=.5)

        #Se devuelve el JSON
        if response:
            return response.json()
    except requests.exceptions.Timeout as err: 
        return "ERROR"

    print(response.text.encode('utf8'))


#Función para extraer el nombre del problema de OIAJ a partir de su link
def extraerProblemNameOIAJ(problem_link):
    #Inicializamos el string que contendrá la respuesta
    problem_name=""

    #Inicializamos la variable que va a recorrer la url
    index=len(problem_link)-1

    #Retrocedemos index hasta que encontremos una /
    while index>=0 and problem_link[index]!='/':
        index-=1

    #Decrementamos una posición para arrancar en la primera letra del nombre
    index-=1

    #Guardo el nombre (hasta que encuentre una barra)
    while index>=0 and problem_link[index]!='/':
        problem_name+=problem_link[index]
        index-=1

    #Devuelvo el string dado vuelta, ya que se recorrió en orden inverso
    return problem_name[::-1]

#Periodic-task
@shared_task
def update_ranking():
    print("UPDATE RANKING")
    
    #Usuarios
    users=User.objects.all()

    #Problemas recomendados
    Recomendados=recommended.objects.all()
    #Problemas DB
    problemas=Problems.objects.all()

    #Por cada usuario
    for user in users:
        #Obtengo la cuenta con nombres de usuario
        cuenta=Account.objects.filter(Logik_Handle=user)

        #Si tiene registrado su usuario de OIAJ
        if  cuenta.exists() and cuenta[0].OIAJ_Handle:
            try:
                #Submissions del usuario
                user_submissions_OIAJ_JSON=submissions_by_user(cuenta[0].OIAJ_Handle)

                #Si los datos se obtuvieron correctamente
                if user_submissions_OIAJ_JSON and 'scores' in user_submissions_OIAJ_JSON:
                    #Problemas de OIAJ submiteados por el usuario
                    resueltos=user_submissions_OIAJ_JSON['scores']
                            
                    #Por cada problema submiteado
                    for task in resueltos:
                        #Nombre de problema
                        task_name=task['name']
                        #Puntos que sacó en el problema
                        task_score=task['score']

                        #Por cada problema de OIAJ
                        for i in problemas:
                            #Si es un problema de OIAJ
                            if i.oiaj==1:
                                #Paso el string a diccionario
                                solved_by=json.loads(i.solvedBy)

                                #Si resolvió el problema
                                if extraerProblemNameOIAJ(i.problem_link)==task_name:
                                    #Actualizo score
                                    solved_by[str(user)]=task_score
                                    
                                    #Hago el update en la DB
                                    Problems.objects.filter(problem_link=i.problem_link).update(solvedBy=json.dumps(solved_by))

                        #Chequear recomendados

                        #Por cada problema de OIAJ
                        for i in Recomendados:
                            #Si es un problema de OIAJ
                            if i.oiaj==1:
                                #Paso el string a diccionario
                                solved_by=json.loads(i.solvedBy)

                                #Si resolvió el problema
                                if extraerProblemNameOIAJ(i.problem_link)==task_name:
                                    #Actualizo score
                                    solved_by[str(user)]=task_score
                                    
                                    #Hago el update en la DB
                                    recommended.objects.filter(problem_link=i.problem_link).update(solvedBy=json.dumps(solved_by))
            except requests.exceptions.Timeout as err: 
                err
            
        #Si tiene registrado su usuario de Codeforces
        if cuenta.exists() and cuenta[0].CF_Handle:
            try:
                #Submissions del usuario
                request_cf=submissions_codeforces(cuenta[0].CF_Handle)
                
                if request_cf and request_cf['status']=='OK':
                    submissions=request_cf['result']

                    #Por cada problema en la DB
                    for problema in problemas:
                        #Si es un problema de Codeforces
                        if problema.oiaj==0:
                            #Paso el string a diccionario
                            solved_by=json.loads(problema.solvedBy)

                            #Reviso todos los submissions
                            for submission in submissions:
                                #Si obtuvo AC en ese problema
                                if (submission['verdict']=='OK' and 
                                    problema.problem_link=='https://codeforces.com/problemset/problem/'+
                                    str(submission['problem']['contestId'])+'/'+
                                    str(submission['problem']['index'])):
                                        #Actualizo score
                                        solved_by[str(user)]=problema.problem_points

                                        #Hago el update en la DB
                                        Problems.objects.filter(problem_link=problema.problem_link).update(solvedBy=json.dumps(solved_by))

                    #Chequeo los problemas recomendados

                    #Por cada problema en la DB
                    for problema in Recomendados:
                        #Si es un problema de Codeforces
                        if problema.oiaj==0:
                            #Paso el string a diccionario
                            solved_by=json.loads(problema.solvedBy)

                            #Reviso todos los submissions
                            for submission in submissions:
                                #Si obtuvo AC en ese problema
                                if (submission['verdict']=='OK' and 'contestId' in submission['problem'] and 
                                    problema.problem_link=='https://codeforces.com/problemset/problem/'+
                                    str(submission['problem']['contestId'])+'/'+
                                    str(submission['problem']['index'])):
                                        #Actualizo score
                                        solved_by[str(user)]=100

                                        #Hago el update en la DB
                                        recommended.objects.filter(problem_link=problema.problem_link).update(solvedBy=json.dumps(solved_by))
            except requests.exceptions.Timeout as err: 
                err