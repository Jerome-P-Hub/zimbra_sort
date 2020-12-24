#!/usr/bin/python
# -*- coding: utf-8 -*-



"""Ce fichier permet de lister les agents présents sur Zimbra

Il s'appuie sur le fichier conf.ini """



from ldap3 import Server, Connection, ALL
import os
import sys
import string
import datetime
import csv



#
# Fonction recup_precedents_utilisateurs
#
# Récupère le fichier csv des comptes Zimbra précédemment présents pour l'enregistrer dans une liste avant suppression (csv recréé lors de la prochaine fonction.
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @return list - Liste des utilisateurs précédents dans Zimbra
#
def recup_precedents_utilisateurs_(cfg):
        # Definition du repertoire de stockage du fichier csv des précédents utilisateurs Zimbra
        dirlist = cfg.get('ZIMBRA', 'zimbra_dis_user_dirlist')
        # Creation de la liste des utilisateurs zimbra précédents
        zimbra_previous_users = []
        # Lecture du fichier .csv qui va récuperer les comptes présents dans zimbra précédemment
        with open ("%sliste_comptes_zimbra_j-1.csv" % dirlist, "r") as in_file:
       		reader = csv.reader (in_file)
		# Pour chaque ligne du fichier
        	for row in reader:
			# Ajout de l'utilisateur à la liste "zimbra_previous_users"
			zimbra_previous_users.append(row[0])
	# Suppression du fichier csv, une fois la liste enregistrée
	os.remove(dirlist + 'liste_comptes_zimbra_j-1.csv')
	# On retourne la liste des utilisateurs zimbra précédents
        return zimbra_previous_users



#
# Fonction recup_utilisateurs
#
# Récupère la liste des comptes actifs dans le serveur Zimbra et enregistre cette liste en csv pour comparaison lors de la prochaine reouverture de script
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @return list - Liste des utilisateurs actifs dans Zimbra
#
def recup_utilisateurs(cfg):
	# Definition des parametres necessaires de connexion au serveur Zimbra
	zimbra_host = cfg.get('ZIMBRA', 'zimbra_host')
	zimbra_login = cfg.get('ZIMBRA', 'zimbra_login')
	zimbra_password = cfg.get('ZIMBRA', 'zimbra_password')
	zimbra_dir_users = cfg.get('ZIMBRA', 'zimbra_dir_users')
	zimbra_filter = cfg.get('ZIMBRA', 'zimbra_filter')
	zimbra_user = cfg.get('ZIMBRA', 'zimbra_user')
	dirlist = cfg.get('ZIMBRA', 'zimbra_dis_user_dirlist') 
	# Definition des methodes de connexion sur le ldap Zimbra
	server =  Server(zimbra_host, get_info=ALL)
	conn_server = Connection(server, zimbra_login, zimbra_password, auto_bind=True)
	# Definition du filtre de recherche sur le ldap Zimbra
	attrs = [zimbra_user]
	conn_server.search(zimbra_dir_users, zimbra_filter, attributes = attrs)
	# Creation d'une liste des utilisateurs zimbra
	zimbra_users = [] 
	# Pour chaque ligne récupérées dans le ldap Zimbra, et pour chaque UID de chaque ligne, on enregistre dans la liste l'uid@ch-tourcoing.fr
	for row in conn_server.entries:
		if zimbra_user in row :
			# Creation d'une variable "mail"
       			mail = ('%s@ch-tourcoing.fr' % (row[zimbra_user]))
			# Ajout de ce compte à la liste "zimbra_users"
			zimbra_users.append(mail.rstrip())
			# Création également d'un fichier .csv qui va stocker les comptes présents dans zimbra, et utilisé lors de la prochaine exécution du script
			with open ("%sliste_comptes_zimbra_j-1.csv" % dirlist, "a") as out_file:
	        		writer = csv.writer (out_file, delimiter =";")
               	       		datas = [mail]
                   		writer.writerow(datas)
	# Renvoi de la liste des utilisateurs zimbra
	return zimbra_users



#
# Fonction recup_zimbra_utilisateurs_a_desactiver
#
# Récupère la liste des comptes Zimbra à desactiver après comparaison entre la liste des utilisateurs desactives dans l'AD et la liste des comptes actifs dans Zimbra
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_a_desactives - Liste des utilisateurs desactives dans l'AD
# @param utilisateurs_zimbra - Liste des comptes actifs dans Zimbra
# @return list - Liste des utilisateurs à desactiver dans Zimbra
#
def recup_zimbra_utilisateurs_a_desactiver(cfg, utilisateurs_ad_desactives, utilisateurs_zimbra):
	# Parcourt de la liste des utilisateurs de l'AD inactifs
	zimbra_dis_users = []
	for inactiv_user in utilisateurs_ad_desactives:
		# A chaque ligne des utilisateurs de l'AD, on parcourt les utilisateurs Zimbra presents dans Zimbra
        	for activ_zimbra_user in utilisateurs_zimbra:
			# Si un utilisateur inactif dans l'AD est present actif dans Zimbra, on le stocke dans une liste
                	if inactiv_user == activ_zimbra_user :
				# Affichage et énoncé du compte à desactiver
                        	print('Compte Zimbra "%s" n\'est plus present dans l\'AD ---> A sortir' ) % inactiv_user
                        	zimbra_dis_users.append(inactiv_user.rstrip())
	# Renvoi de la liste des utilisateurs à desactiver
	return	zimbra_dis_users		



#
# Fonction desactivation_utilisateurs_zimbra
#
# Crée une liste des utilisateurs qui vont etre desactivés puis lance la commande pour les désactiver si le test à blanc est désactivé 
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_zimbra_a_desactiver - Liste des utilisateurs à desactiver dans Zimbra
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return
#
def desactivation_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun):
	# Definition des commandes systèmes utilisees par Zimbra
	date = datetime.datetime.now()
	year = date.year
	month = date.month
	day = date.day
	hour = date.hour
	minute = date.minute
	dirlist = cfg.get('ZIMBRA', 'zimbra_dis_user_dirlist') 
	zcmd_dis_user = cfg.get('ZIMBRA', 'zcmd_dis_user')
	# Parcourt de la liste des utilisateurs Zimbra qui doivent être désactivés
	for user in utilisateurs_zimbra_a_desactiver:
		# Récuperation de la commande à executer sur le compte
		desactivation = zcmd_dis_user % user
		# Affichage de la commande et le compte sur lequel le script va s'executer
		print ('Commande a effectuer pour desactivation: %s') % desactivation
		if not dryrun:
			# Exécution de la commande Zimbra
               		os.system(desactivation)
			# Affichage de l'utilisateur maintenant désactivé	
			print ('Utilisateur "%s" a present desactive') % user
			# Création d'un fichier .csv qui va récuperer l'année, le mois, la date, l'heure, les minutes de l'éxécution du script ainsi que le compte associé désactivé
			with open ("%sliste_agents_desactives.csv" % dirlist, "a") as out_file:
	       			writer = csv.writer (out_file, delimiter =";")
                     		datas = [year,month,day,hour,minute,user]
                   		writer.writerow(datas)
	return



#
# Fonction suppression_utilisateurs_zimbra
#
# Supprime les utilisateurs initialement désactivés avec bakcup archive  si le test à blanc est désactivé et enregistre la date-heure et le nom des agents supprimés
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_zimbra_a_desactiver - Liste des utilisateurs à supprimer dans Zimbra
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return
#
def suppression_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun):
	# Definition des commandes systèmes utilisees par Zimbra
	date = datetime.datetime.now()
	year = date.year
	month = date.month
	day = date.day
	hour = date.hour
	minute = date.minute
	dirlist = cfg.get('ZIMBRA', 'zimbra_dis_user_dirlist') 
	zcmd_del_user = cfg.get('ZIMBRA', 'zcmd_del_user')
	# Parcourt de la liste des utilisateurs Zimbra qui doivent être désactivés
	for user in utilisateurs_zimbra_a_desactiver:
		# Récuperation de la commande à executer sur le compte
		suppression = zcmd_del_user % user
		# Affichage de la commande et le compte sur lequel le script va s'executer
		print ('Commande a effectuer pour suppression de: %s') % suppression
		if not dryrun:
			# Exécution de la commande Zimbra
               		os.system(suppression)
			# Affichage de l'utilisateur maintenant désactivé	
			print ('Utilisateur "%s" a present supprimé de Zimbra') % user
			# Création un fichier .csv qui va récuperer l'année, le mois, la date, l'heure, les minutes de l'éxécution du script ainsi que le compte associé désactivé
			with open ("%sliste_agents_supprimes.csv" % dirlist, "a") as out_file:
	        		writer = csv.writer (out_file, delimiter =";")
               	       		datas = [year,month,day,hour,minute,user]
                   		writer.writerow(datas)
	return 


