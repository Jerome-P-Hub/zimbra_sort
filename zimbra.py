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
# Fonction recup_utilisateurs
#
# Récupère la liste des comptes actifs dans le serveur Zimbra
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @return list - Liste des utilisateurs actifs dans Zimbra
#
def recup_utilisateurs(cfg):
	# On definit les parametres necessaires de connexion au serveur Zimbra
	zimbra_host = cfg.get('ZIMBRA', 'zimbra_host')
	zimbra_login = cfg.get('ZIMBRA', 'zimbra_login')
	zimbra_password = cfg.get('ZIMBRA', 'zimbra_password')
	zimbra_dir_users = cfg.get('ZIMBRA', 'zimbra_dir_users')
	zimbra_filter = cfg.get('ZIMBRA', 'zimbra_filter')
	zimbra_user = cfg.get('ZIMBRA', 'zimbra_user')
	# On definit les methodes de connexion sur le ldap Zimbra
	server =  Server(zimbra_host, get_info=ALL)
	conn_server = Connection(server, zimbra_login, zimbra_password, auto_bind=True)
	# On definit le filtre de recherche sur le ldap Zimbra
	attrs = [zimbra_user]
	conn_server.search(zimbra_dir_users, zimbra_filter, attributes = attrs)
	# Creation de liste des utilisateurs zimbra
	zimbra_users = [] 
	# Pour chaque ligne récupérées dans le ldap Zimbra, et pour chaque UID de chaque ligne, on enregistre dans la liste l'uid@ch-tourcoing.fr
	for row in conn_server.entries:
		if zimbra_user in row :
       			mail = ('%s@ch-tourcoing.fr' % (row[zimbra_user]))
			zimbra_users.append(mail.rstrip())
	# On retourne la liste des utilisateurs zimbra
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
	# On parcourt la liste des utilisateurs de l'AD inactifs
	zimbra_dis_users = []
	for inactiv_user in utilisateurs_ad_desactives:
		# A chaque ligne des utilisateurs de l'AD, on parcourt les utilisateurs Zimbra presents dans Zimbra
        	for activ_zimbra_user in utilisateurs_zimbra:
			# Si un utilisateur inactif dans l'AD est present actif dans Zimbra, on le stocke dans une liste
                	if inactiv_user == activ_zimbra_user :
                        	print('Compte Zimbra "%s" n\'est plus present dans l\'AD ---> A sortir' ) % inactiv_user
                        	zimbra_dis_users.append(inactiv_user.rstrip())
	# on retourne la liste des utilisateurs à desactiver
	return	zimbra_dis_users		



#
# Fonction desactivation_utilisateurs_zimbra
#
# Crée une liste des utilisateurs qui vont etre desactivés puis lance la commande pour les désactiver si le test à blanc est désactivé 
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_zimbra_a_desactiver - Liste des utilisateurs à desactiver dans Zimbra
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas
# @return  - Retoune la commande exécutée pour desactiver l'utilisateur dans Zimbra
#
def desactivation_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun):
	# On definit les commandes systèmes utilisees par Zimbra
	date = datetime.datetime.now()
	year = date.year
	month = date.month
	day = date.day
	hour = date.hour
	minute = date.minute
	dirlist = cfg.get('ZIMBRA', 'zimbra_dis_user_dirlist') 
	zcmd_dis_user = cfg.get('ZIMBRA', 'zcmd_dis_user')
	# On parcourt la liste des utilisateurs Zimbra qui doivent être désactivés
	for user in utilisateurs_zimbra_a_desactiver:
		# On récupere la commande à executer sur le compte
		desactivation = zcmd_dis_user % user
		# On affiche la commande et le compte sur lequel le script va s'executer
		print ('Commande a effectuer pour desactivation: %s') % desactivation
		if not dryrun:
			# On exécute la commande Zimbra
               		os.system(desactivation)
			# On affiche l'utilisateur maintenant désactivé	
			print ('Utilisateur "%s" a present desactive') % user
			# On crée un fichier .csv qui va récuperer l'année, le mois, la date, l'heure, les minutes de l'éxéution du script ainsi que le compte associé maintenant désactivé
			with open ("%sliste_agents_desactives.csv" % dirlist, "a") as out_file:
	        		writer = csv.writer (out_file, delimiter =";")
               	       		datas = [year,month,day,hour,minute,user]
                   		writer.writerow(datas)
		# On retourne la commande de desactivation
		return desactivation
