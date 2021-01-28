#!/usr/bin/python
# -*- coding: utf-8 -*-




"""
archiv.py

Ce script archive dans un dossier temporaire la BAL des utilisateurs desactivés, puis copie la BAL compressée sur un lecteur réseau partagé pour retention du fichier.
Il supprime apres quelques temps le fichier compressé dans le repertoire temporaire et compare egalement les BAL archivées avec les nouveaux utilisateurs zimbra pour reincorporer si l'utilisateur est deja venu son ancienne archive. 

Author: Jerome Plewa
Version: 1.0
Date: 12/2020

Il charge et utilise le fichier conf.ini contenant les differents parametres obligatoires
"""





import os
import sys
import string
import time
import datetime
import csv
import glob
import shutil
from logs import *



#
# Fonction archivage_utilisateur_zimbra
#
# Exécute la commande pour archiver temporairement (definie par une valeur "archiv_tmp_dir_duration" dans le fichier conf.ini) dans un format .tgz les BAL concernées
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_zimbra_a_desactiver - Liste des utilisateurs a desactiver dans Zimbra
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return - Reto# Verification du boolen dryrun puis execution de la commande si dryrun défini sur falseurne la commande pour créer l'archive .tgz des utilisateurs Zimbra à désactiver
#
def archivage_utilisateur_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun):
        # Definition des commandes systèmes utilisees par Zimbra
	archiv_tmp_dir = cfg.get('ARCHIVAGE', 'archiv_tmp_dir')
	archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
	# Recuperation de la commande de base Zimbra pour archiver une BAL en .tgz
        zcmd_archiv_user = cfg.get('ARCHIVAGE', 'zcmd_archiv_user')
	# Parcourt de la liste des utilisateurs Zimbra a desactiver
        for user in utilisateurs_zimbra_a_desactiver:
		# Création de la commande personnalisée à l'utilisateur
               	archivage = zcmd_archiv_user % (user, archiv_tmp_dir, user)
		# Affichage de la commande à exécuter pour archiver la BAL
		log("INFO", "archiv", "Commande zimbra utilisée pour générer l'archive de l'utilisateur: %s" % (archivage))
                # Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
		if not dryrun:
			# On exécute la commande Zimbra	
                        os.system(archivage)
			# On affiche que l'archive de l'utilisateur est maintenant créée
			log("INFO", "archiv", "Archive de l'utilisateur '%s' correctement créée" % (user))
       	return 



#
# Fonction list_tmp_archivage
#
# Crée une liste des fichiers .tgz dans le repertoire temporaire si ceux-ci sont plus agés que la variable définie "archiv_tmp_dir_duration" (en secondes) enregistrée dans le fichier conf.ini
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_zimbra_a_desactiver - Liste des utilisateurs a desactiver dans Zimbra
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return list - Retourne la commande pour créer l'archive .tgz des utilisateurs Zimbra à désactiver
#
def list_tmp_archivage(cfg, utilisateurs_zimbra_a_desactiver, dryrun):
	# Création des variables associées au temps 
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
	actual_time = time.time()
	# Création des variables necessaires et liés aux commandes systèmes Zimbra d'archivage
	archiv_tmp_dir = cfg.get('ARCHIVAGE', 'archiv_tmp_dir')
        archiv_tmp_dir_duration = cfg.get('ARCHIVAGE', 'archiv_tmp_dir_duration')
	archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
	archiv_list = cfg.get('ARCHIVAGE', 'archiv_list')
	# Création d' une liste pour récupérer les fichiers .tgz plus anciens qu'attendue
	liste_fichiers_tmp = []
	# Parcourt des fichiers .tgz du répertoire concerné
	log("INFO", "archiv", "Analyse des archives actuellement sauvegardées dans le répertoire temporaire")
	for somefile in glob.glob (archiv_tmp_dir + '/*'):
		log("INFO", "archiv", "Archive '%s' présente dans le répertoire temporaire" % (somefile))
		# Création d'une variable qui récupere la date de modification du fichier
		mtime = os.path.getmtime (somefile)
		# Création d'une variable de la difference entre la date d'aujourd'hui et celle de modification du fichier
		delta = actual_time - mtime
		# Si ce delta est supérieur à celui attendu, défini dans le fichier conf.ini, alors on affiche le fichier avec son chemin et on l'enregistre dans la liste prévue
		if delta > float(archiv_tmp_dir_duration) :
			# Affichage du fichier trop ancien amené a être supprimé
			log("INFO", "archiv", "Cette archive '%s' dépasse le temps limite de sauvegarde dans le répertoire temporaire, demande de suppression en cours..." % (somefile))
			liste_fichiers_tmp.append(somefile)
	# On retourne la liste des fichiers .tgz à effacer du dossier temporaire	
	return liste_fichiers_tmp
			


# Fonction suppr_tmp_archivage
#
# Supprime les fichiers compressés .tgz, trop vieux (defini dans le fichier conf.ini) du repertoire temporaire
#
# @param list_tmp_archivage - Liste des fichiers .tgz à supprimer du répertoire temporaire
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return 
#
def suppr_tmp_archivage(list_tmp_archivage, dryrun):
	# Parcourt de chaque ligne de la liste
	for somefile in list_tmp_archivage:
		# Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
		if not dryrun:
			log("INFO", "archiv", "Suppression de l'archive '%s' dans le répertoire temporaire..." % (somefile))
			# Execution de la commande de suppression du fichier .tgz trop vieux
			os.remove(somefile)
			# Affichage de la suppression du fichier concerné
			log("INFO", "archiv", "Archive temporaire '%s' correctement supprimé" % (somefile))
	return



# Fonction copy_tmp_archivage
#
# Copie les fichiers compressés .tgz, du repertoire temporaire, vers le montage réseau pour sauvegarde perenne
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return 
#
def copy_tmp_archivage(cfg, dryrun):
	# Création des variables necessaires et liées aux commandes systèmes Zimbra d'archivage
        archiv_tmp_dir = cfg.get('ARCHIVAGE', 'archiv_tmp_dir')
        archiv_tmp_dir_duration = cfg.get('ARCHIVAGE', 'archiv_tmp_dir_duration')
        archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
        archiv_list = cfg.get('ARCHIVAGE', 'archiv_list')
        archiv_chown = cfg.get('ARCHIVAGE', 'archiv_chown')
	# Parcourt du repertoire transmis avec liste de chaque fichier
	src_files = os.listdir(archiv_tmp_dir)
	# Pour chaque fichier dans le repertoire
	for somefile in src_files:
		# Creation de la variable qui s'approprie les fichiers compressés 
		chown = archiv_chown % (archiv_dir, somefile)
		# Creation du chemin complet du fichier	en variable
       		full_file_name = os.path.join(archiv_tmp_dir, somefile)
		# Si le fichier compressé existe
       		if (os.path.isfile(full_file_name)):
			# Copie du fichier du repertoire temporaire vers le repertoire de sauvegarde perenne
           		shutil.copy(full_file_name, archiv_dir)
			# Attribution des droits sur l'archive dans le dossier perenne, necessaire a un potentiel import furtur
			os.system(chown)
			# Affichage de la l'execution de la copie vers le repertoire perenne
			log("INFO", "archiv", "Archive '%s%s' correctement transféré vers '%s%s'" % (archiv_tmp_dir, somefile, archiv_dir, somefile))
	return 




#
# Fonction list_archivage
#
# Crée une liste des fichiers .tgz dans le repertoire d'archive si ceux-ci sont plus agés que la variable définie "archiv_duration" (en secondes) enregistrée dans le fichier conf.ini
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return list - Retourne la liste des archives .tgz à supprimer car plus necessaire de sauvegarder
#
def list_archivage(cfg, dryrun):
	# Création des variables associées au temps 
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
	actual_time = time.time()
	# Création des variables necessaires et liés aux commandes systèmes Zimbra d'archivage
        archiv_duration = cfg.get('ARCHIVAGE', 'archiv_duration')
	archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
	# Création d'une liste pour récupérer les fichiers .tgz plus vieux qu'attendue
	liste_fichiers_archive = []
	# Parcourt les fichiers .tgz du répertoire concerné
	for somefile in glob.glob (archiv_dir + '/*'):
		# Création d'une variable qui récupere la date de modification du fichier
		mtime_archive = os.path.getmtime (somefile)
		# Création d'une variable de la difference entre la date d'aujourd'hui et celle de modification du fichier
		delta = actual_time - mtime_archive
		# Si ce delta est supérieur à celui attendu, défini dans le fichier conf.ini, alors on affiche le fichier avec son chemin et on l'enregistre dans la liste prévue
		if delta > float(archiv_duration) :
			liste_fichiers_archive.append(somefile)
	# Renvoie de la liste des fichiers .tgz à supprimer du dossier temporaire	
	return liste_fichiers_archive





# Fonction suppr_archivage
#
# Supprime les fichiers compressés .tgz, trop vieux (défini en secondes dans le fichier conf.ini), du repertoire d'archives
#
# @param liste_archivage - Liste des fichiers .tgz à supprimer du répertoire temporaire
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return 
#
def suppr_archivage(liste_archivage, dryrun):
	# Parcourt de chaque ligne de la liste
	for somefile in liste_archivage:
		# Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
		if not dryrun:
		# Execution de la commande de suppression du fichier .tgz trop vieux
			os.remove(somefile)
	return	



# Fonction liste_nouveaux
#
# Compare le fchier des précédents présents Zimbra avec l'actuel et crée une liste avec les nouveaux utilisateurs Zimbra
#
# @param recup_precedents_utilisateurs - Récupere la liste des utilisateurs Zimbra précédents
# @param utilisateurs_zimbra - Récupère la liste des utilisateurs actuels
# @return list - Liste des nouveaux utilisateurs Zimbra
#
def liste_nouveaux(recup_precedents_utilisateurs, utilisateurs_zimbra):
	# On transforme les 2 listes en set pour pouvoir effectuer une comparaison
	s1 = set(recup_precedents_utilisateurs)
	s2 = set(utilisateurs_zimbra)
	# Declaration d'une nouvelle liste qui enregistrera les nouveaux utilisateurs apparus dans Zimbra
	new_users = []
	# Soustraction des deux liste pour récuperer uniquement les nouveaux utilisateurs Zimbra
	diff = s2 - s1
	# Affichage et enregistrement de chaque utilisateur dans la liste "new_users" 
	for user in diff:
		new_users.append(user)
		log("INFO", "archiv", "Nouvel utilisateur Zimbra détecté : '%s'" % (user))
	# Renvoi de la liste "new_users" à la fonction
	return new_users



#
# Fonction ajout_archive
#
# Verifie si, pour un nouvel utilisateur Zimbra, une sauvegarde précédente lui est associé et si oui, la réimporte.
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param liste_nouveaux - Liste des nouveaux utilisateurs Zimbra
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return 
#

def ajout_archive(cfg, liste_nouveaux, dryrun):
	# Recuperation des parametres necessaires tel que le repertoire d'archivage et la commande zimbra d'import 
	archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
	zcmd_add_archiv_user = cfg.get('ARCHIVAGE', 'zcmd_add_archiv_user')
	# Pour chaque utilisateur dans la liste  	
	for user in liste_nouveaux:
		# creation du chemin complet vers le fichier correspondant à l'utilisateur
		dest = "%s%s.tar.gz" % (archiv_dir, user)
		# Verification que le fichier existe bien pour cet utilisateur
		if os.path.isfile(dest):
			# Creation de la commande d'import pour l'utilisateur 
			ajout = zcmd_add_archiv_user % (user, archiv_dir, user)
			# Affichage de la commande lancée
			log("INFO", "archiv", "Le Nouvel utilisateur Zimbra '%s' possède une sauvegarde de sa BAL" % (user))
			# Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
			if not dryrun:
				log("INFO", "archiv", "Commande Zimbra pour incorporation de la sauvegarde dans la BAL: '%s'" % (ajout))
				os.system(ajout)
				log("INFO", "archiv", "Archive '%s' correctement ajouté la BAL '%s'" % (dest, user))
	return	
	







