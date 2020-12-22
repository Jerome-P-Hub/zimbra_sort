#!/usr/bin/python
# -*- coding: utf-8 -*-




"""Ce fichier permet de lister les agents présents sur Zimbra

Il s'appuie sur le fichier conf.ini """



import os
import sys
import string
import time
import datetime
import csv
import glob




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
        # On definit les commandes systèmes utilisees par Zimbra
	archiv_tmp_dir = cfg.get('ARCHIVAGE', 'archiv_tmp_dir')
	archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
	# On recupere la commande de base Zimbra pour archiver une BAL en .tgz
        zcmd_archiv_user = cfg.get('ARCHIVAGE', 'zcmd_archiv_user')
	# On parcourt la liste des utilisateurs Zimbra a desactiver
        for user in utilisateurs_zimbra_a_desactiver:
		# On crée la commande personnalisée à l'utilisateur
               	archivage = zcmd_archiv_user % (user, archiv_tmp_dir, user)
		# On affiche la commande à exécuter pour archiver la BAL
                print ('Commande a effectuer pour creer l\'archive: %s') % archivage
                # Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
		if not dryrun:
			# On exécute la commande Zimbra	
                        os.system(archivage)
			# On affiche que l'archive de l'utilisateur est maintenant créée
                        print ('Archive de l\'Utilisateur "%s" créée') % user
		# On retourne la commande d'archivage de la BAL
       		return archivage



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
	# On crée des variables associées au temps 
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
	actual_time = time.time()
	# On crée des variables necessaires et liés aux commandes systèmes Zimbra d'archivage
	archiv_tmp_dir = cfg.get('ARCHIVAGE', 'archiv_tmp_dir')
        archiv_tmp_dir_duration = cfg.get('ARCHIVAGE', 'archiv_tmp_dir_duration')
	archiv_dir = cfg.get('ARCHIVAGE', 'archiv_dir')
	archiv_list = cfg.get('ARCHIVAGE', 'archiv_list')
	# On crée une liste pour récupérer les fichiers .tgz plus vieux qu'attendue
	liste_fichiers_tmp = []
	# On parcourt les fichiers .tgz du répertoire concerné
	for somefile in glob.glob (archiv_tmp_dir + '/*'):
		# On crée une variable qui récupere la date de modification du fichier
		mtime = os.path.getmtime (somefile)
		# On crée une variable de la difference entre la date d'aujourd'hui et celle de modification du fichier
		delta = actual_time - mtime
		# Si ce delta est supérieur à celui attendu, défini dans le fichier conf.ini, alors on affiche le fichier avec son chemin et on l'enregistre dans la liste prévue
		if delta > float(archiv_tmp_dir_duration) :
			print (somefile)
			liste_fichiers_tmp.append(somefile)
	# On retourne la liste des fichiers .tgz à effacer du dossier temporaire	
	return liste_fichiers_tmp
			


# Fonction suppr_tmp_archivage
#
# Supprime les fichiers compressés .tgz, trop vieux, du repertoire temporaire
#
# @param list_tmp_archivage - Liste des fichiers .tgz à supprimer du répertoire temporaire
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return 
#
def suppr_tmp_archivage(list_tmp_archivage, dryrun):
	# On parcourt chaque ligne de la liste
	for somefile in list_tmp_archivage:
		# Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
		if not dryrun:
		# Execution de la commande de suppression du fichier .tgz trop vieux
			os.remove(somefile)
	return






