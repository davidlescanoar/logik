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
from logik.oiaj import *
from logik.codeforces import *
from logik.cses import *
from logik.spoj import *
from logik.OnlineJudge import *

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from logik.settings import EMAIL_HOST_USER as sender
from logik.settings import LOGIK_EMAIL as logikEmail
from django.conf import settings


def vaciarSolvedBy():
    for p in Problems.objects.all():
        Problems.objects.filter(problem_link=p.problem_link).update(solvedBy="{}")  # Hago el update en la DB

    for p in Recommended.objects.all():
        Recommended.objects.filter(problem_link=p.problem_link).update(solvedBy="{}")  # Hago el update en la DB


@shared_task
def validarCuentas(fechaNow, CF_Handle_Input, OIAJ_Handle_Input, CSES_Handle_Input, SPOJ_Handle_Input,
                   OnlineJudge_Handle_Input, UserID, Username):
    validarCuentaCodeforces(CF_Handle_Input, UserID, Username, fechaNow)
    validarCuentaOIAJ(OIAJ_Handle_Input, UserID, Username, fechaNow)
    actualizarCuentaCSES(CSES_Handle_Input, UserID, Username, fechaNow)
    actualizarCuentaSPOJ(SPOJ_Handle_Input, UserID, Username, fechaNow)
    actualizarCuentaOnlineJudge(OnlineJudge_Handle_Input, UserID, Username, fechaNow)


# Periodic-task
@shared_task
def update_ranking(CF_submissions_count=20):
    # Usuarios
    users = User.objects.all()

    for user in users:
        cuenta = Account.objects.get(Logik_Handle=user)
        if cuenta.exists():
            # Update OIAJ
            if cuenta.OIAJ_Handle:
                #print("Llamando a la funcion update_OIAJ para user {} ({})".format(cuenta.OIAJ_Handle, user))
                try:
                    request_oiaj = submissions_OIAJ(cuenta.OIAJ_Handle)
                    try:
                        update_OIAJ(user, Problems, request_oiaj)
                        update_OIAJ(user, Recommended, request_oiaj)
                    except BaseException as e:
                        pass
                        #print("Error con el usuario {} ({}) al llamar update_OIAJ. Error: {}".format(
                            #cuenta.OIAJ_Handle, user, str(e)))
                except BaseException as e:
                    pass
                    #print("Error en update_ranking: {}".format(str(e)))

            # Update Codeforces
            if cuenta.CF_Handle:
                #print("Llamando a la funcion update_Codeforces para user {} ({})".format(cuenta.CF_Handle, user))
                try:
                    request_cf = submissions_codeforces(cuenta.CF_Handle, CF_submissions_count)
                    try:
                        update_Codeforces(user, Problems, request_cf)
                        update_Codeforces(user, Recommended, request_cf)
                    except BaseException as e:
                        pass
                        #print("Error con el usuario {} ({}) al llamar update_Codeforces. Error: {}".format(
                            #cuenta.CF_Handle, user, str(e)))
                except BaseException as e:
                    pass
                    #print("Error en update_ranking: {}".format(str(e)))

            # Update CSES
            if cuenta.CSES_Handle:
                #print("Llamando a la funcion update_CSES para user {} ({})".format(cuenta.CSES_Handle, user))
                try:
                    request_cses = submissions_CSES(cuenta.CSES_Handle)
                    try:
                        update_CSES(user, Problems, request_cses)
                        update_CSES(user, Recommended, request_cses)
                    except BaseException as e:
                        pass
                        #print("Error con el usuario {} ({}) al llamar update_CSES. Error: {}".format(
                            #cuenta.CSES_Handle, user, str(e)))
                except BaseException as e:
                    pass
                    #print("Error en update_ranking: {}".format(str(e)))

            # Update SPOJ
            if cuenta.SPOJ_Handle:
                #print("Llamando a la funcion update_SPOJ para user {} ({})".format(cuenta.SPOJ_Handle, user))
                try:
                    request_spoj = submissions_SPOJ(cuenta.SPOJ_Handle)
                    try:
                        update_SPOJ(user, Problems, request_spoj)
                        update_SPOJ(user, Recommended, request_spoj)
                    except BaseException as e:
                        pass
                        #print("Error con el usuario {} ({}) al llamar update_SPOJ. Error: {}".format(
                            #cuenta.SPOJ_Handle, user, str(e)))
                except BaseException as e:
                    pass
                    #print("Error en update_ranking: {}".format(str(e)))

            # Update OnlineJudge
            if cuenta.OnlineJudge_Handle:
                #print("Llamando a la funcion update_OnlineJudge para user {} ({})".format(cuenta.OnlineJudge_Handle,
                                                                                          user))
                try:
                    request_OnlineJudge = submissions_OnlineJudge(cuenta.OnlineJudge_Handle)
                    try:
                        update_OnlineJudge(user, Problems, request_OnlineJudge)
                        update_OnlineJudge(user, Recommended, request_OnlineJudge)
                    except BaseException as e:
                        pass
                        #print("Error con el usuario {} ({}) al llamar update_OnlineJudge. Error: {}".format(
                            #cuenta.OnlineJudge_Handle, user, str(e)))
                except BaseException as e:
                    pass
                    #print("Error en update_ranking: {}".format(str(e)))


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


@receiver(post_save, sender=Problems, dispatch_uid="update_solved_new_problem")
def update_solved_new_problem(sender, instance, **kwargs):
    #print("Llamando a update_ranking porque agregue un problema nuevo")
    update_ranking.apply_async([200000], countdown=10)


@receiver(post_save, sender=Recommended, dispatch_uid="update_solved_new_recommended")
def update_solved_new_recommended(sender, instance, **kwargs):
    #print("Llamando a update_ranking porque agregue un recomendado nuevo")
    update_ranking.apply_async([200000], countdown=10)


@shared_task
def sendEmail(contact):
    subject = 'Logik - Nuevo mensaje'
    body = contact
    send_mail(subject, body, sender, [logikEmail])
