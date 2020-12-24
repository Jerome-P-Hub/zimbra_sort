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
	# Definition des parametres necessaires de connexion AD
	ad_host = cfg.get('AD', 'ad_host')
	ad_login = cfg.get('AD', 'ad_login')
	ad_password = cfg.get('AD', 'ad_password')
	ad_dir_disabled_users = cfg.get('AD', 'ad_dir_disabled_users')
	ad_filter = cfg.get('AD', 'ad_filter')
	ad_user = cfg.get('AD', 'ad_user')
	ad_alias = cfg.get('AD', 'ad_alias')
	# Definition des methodes de connexion sur l'AD
	server =  Server(ad_host, get_info=ALL)
	conn_server = Connection(server, ad_login, ad_password, auto_bind=True)
	# Definition du filtre de recherche sur l'AD
	attrs = [ad_user, ad_alias]
	conn_server.search(ad_dir_disabled_users, ad_filter, attributes = attrs)
	disabled_users = [] 
	# Parcourt des lignes de chaque compte récupérés dans l'AD
	for row in conn_server.entries:
		# Si Attribut de l'AD present dans la ligne
		if ad_user in row :
			# Creation d'une variable 'mail'
	    		mail = ('%s@ch-tourcoing.fr' % (row[ad_user]))
			# Ajout du mail de l'utilisateur desactivé à la liste
			disabled_users.append(mail.rstrip())
	# On retourne la liste des utilisateurs AD désactivés
	return disabled_users
	



