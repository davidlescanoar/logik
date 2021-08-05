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
import sys

def submissions_SPOJ(SPOJ_ID):
    try:
        SPOJ_URL = "https://www.spoj.com/users/{}/".format(SPOJ_ID)
        response = requests.request("GET", SPOJ_URL, data={}, timeout=2)
        soup = BeautifulSoup(response.content, "html.parser")
        tablas = soup.findAll("div", attrs = {"id" : "user-profile-tables"})[0].findAll("table")
        accepted = dict(("https://www.spoj.com/problems/" + x.text + "/", 100) for x in tablas[0].findAll("a", text=True))
        failed = dict(("https://www.spoj.com/problems/" + x.text + "/", 0) for x in tablas[1].findAll("a", text=True))
        return {**accepted, **failed}
    except BaseException as e:
        raise ValueError("Funcion API: submissions_SPOJ. Error: {}".format(str(e)))


def update_SPOJ(user, database, envios):
    if not envios:
        raise ValueError("Error al llamar a API de SPOJ")

    #Envios es un diccionario (link, puntaje) de envios a SPOJ
    problemas = database.objects.filter(judge = 'SPOJ')
    validos = [(p, envios[r]) for p in problemas for r in envios if p.problem_link == r]

    for p in validos:
        solved_by = json.loads(p[0].solvedBy) # Convierto a dict
        solved_by[str(user)] = p[1] # Actualizo score
        database.objects.filter(problem_link=p[0].problem_link).update(solvedBy=json.dumps(solved_by)) # Hago el update en la DB


#Actualizar cuenta de SPOJ
def actualizarCuentaSPOJ(SPOJ_Handle_Input, UserID, Logik_Handle, fNow):
    if len(str(SPOJ_Handle_Input)) < 1:
        return "Campo SPOJ_Handle_Input vacio"

    try:
        if Account.objects.filter(AccountID=UserID).exists():
            Account.objects.filter(AccountID=UserID).update(SPOJ_Handle=SPOJ_Handle_Input)
        #Si no existía en la DB, lo inserto
        else:
            Account.objects.create(AccountID=UserID, Logik_Handle=Logik_Handle, SPOJ_Handle=SPOJ_Handle_Input)

        #print("Usuario {} asoció su handle de SPOJ: {}".format(Logik_Handle, SPOJ_Handle_Input))
        request_spoj = submissions_SPOJ(SPOJ_Handle_Input)
        update_SPOJ(Logik_Handle, Problems, request_spoj)
        update_SPOJ(Logik_Handle, Recommended, request_spoj)
        #print("Usuario {} actualizo correctamente todos los submissions de SPOJ: {}".format(Logik_Handle, SPOJ_Handle_Input))
    except BaseException as e:
        pass
        #print("Error al asociar cuenta de SPOJ: {}".format(str(e)))
