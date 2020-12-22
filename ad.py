#!/usr/bin/python
# -*- coding: utf-8 -*-



"""Ce fichier permet de lister les agents inactifs sur l'AD

Il s'appuie sur le fichier conf.ini """



from ldap3 import Server, Connection, ALL
import os
import sys
import string



#
# Fonction recup_utilisateurs_inactifs
#
# Récupère la liste des utilisateurs AD désactivés 
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @return list - Liste des utilisateurs désactivés dans l'AD
#
def recup_utilisateurs_inactifs(cfg):
	""" Fonction chargée de récupérer les utilisateurs inactifs de l'AD"""
	# On definit les parametres necessaires de connexion AD
	ad_host = cfg.get('AD', 'ad_host')
	ad_login = cfg.get('AD', 'ad_login')
	ad_password = cfg.get('AD', 'ad_password')
	ad_dir_disabled_users = cfg.get('AD', 'ad_dir_disabled_users')
	ad_filter = cfg.get('AD', 'ad_filter')
	ad_user = cfg.get('AD', 'ad_user')
	ad_alias = cfg.get('AD', 'ad_alias')
	# On definit les methodes de connexion sur l'AD
	server =  Server(ad_host, get_info=ALL)
	conn_server = Connection(server, ad_login, ad_password, auto_bind=True)
	# On definit le filtre de recherche sur l'AD
	attrs = [ad_user, ad_alias]
	conn_server.search(ad_dir_disabled_users, ad_filter, attributes = attrs)
	disabled_users = [] 
	# On parcourt les lignes de chaque compte récupérés dans l'AD, et on ajoute
	for row in conn_server.entries:
		if ad_user in row :
	    		mail = ('%s@ch-tourcoing.fr' % (row[ad_user]))
			disabled_users.append(mail.rstrip())
	# On retourne la liste des utilisateurs AD désactivés
	return disabled_users
	



