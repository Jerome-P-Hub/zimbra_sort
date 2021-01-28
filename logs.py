#!/usr/bin/python
# -*- coding: utf-8 -*-




"""
logs.py

Ce script genere les logs, date, type, message et les transfère au fonctions exterieures qui en font appel.


Author: Jerome Plewa
Version: 1.0
Date: 01/2021

Il charge et utilise le fichier conf.ini contenant les differents parametres obligatoires
"""





import time
import datetime

logPath= ""


#
# Fonction logs_time
#
# Génère le temps actuel pour les logs
#
# @return var - Date et Horaire actuel
#
def logs_time():
        # Definition des variables de temps 
	date = datetime.datetime.now()
        year = date.year
        month = '{:02d}'.format(date.month)
        day = '{:02d}'.format(date.day)
        hour = '{:02d}'.format(date.hour)
        minute = '{:02d}'.format(date.minute)
      	second = '{:02d}'.format(date.second)
	h_log = "%s-%s-%s %s:%s:%s" % (year, month, day, hour, minute, second)
	return h_log


#
# Fonction logs
#
# Définit et Génère les logs, les affiche et les enregistre dans un fichier texte
#
# @return 
#
def log(level, module, msg):
	# Definition de la ligne de log à écrire reprenant les différents arguments
	line = "%s [%s] - (%s) --- %s" % (logs_time(), level, module, msg)
	# Affiche la ligne de log
	print (line)
	# Definition d'une variable faisant l'appel à l'ouverture d'un fichier (nom du fichier, option ajout)
 	df = open(logPath, "a") 
	# Ecriture de la variable "line" dans ce fichier
       	df.write(line + '\n')
	# Fermeture, enregistrement du fichier
	df.close()
	

