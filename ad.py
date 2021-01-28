#!/usr/bin/python
# -*- coding: utf-8 -*-




"""
ad.py

Ce script permet de lister les agents inactifs sur l'AD

Author: Jerome Plewa
Version: 1.0
Date: 12/2020

Il charge et utilise le fichier conf.ini contenant les differents parametres obligatoires

Il s'appuie sur le fichier conf.ini
 """



from ldap3 import Server, Connection, ALL
import os
import sys
import string
from logs import *





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
	ad_domain = cfg.get('AD', 'ad_domain')
	try:
        	# Creation d'une liste de stockage des utilisateurs desactivés
        	disabled_users = []
		# Definition de l'accès serveur pour connexion sur l'AD
		server =  Server(ad_host, get_info=ALL)
		#Connexion sur l'AD
		conn_server = Connection(server, ad_login, ad_password, auto_bind=True)
		log("INFO", "ad", "Connexion établie sur l'annuaire AD")
		# Definition des attributs du filtre de recherche sur l'AD
		attrs = [ad_user, ad_alias]
		# Recherche sur l'AD
		conn_server.search(ad_dir_disabled_users, ad_filter, attributes = attrs)
		log("INFO", "ad", "Récupération des utilisateurs désactivés")
		# Parcourt des lignes de chaque compte récupérés dans l'AD
		for row in conn_server.entries:
			# Si Attribut de l'AD present dans la ligne
			if ad_user in row :
				# Creation d'une variable 'mail'
	    			mail = ('%s%s' % (row[ad_user], ad_domain))
				# Ajout du mail de l'utilisateur desactivé à la liste
				disabled_users.append(mail.rstrip())
		# On retourne la liste des utilisateurs AD désactivés
		return disabled_users
	except :
		log("ERROR", "ad", "Vérifier la connexion au serveur AD - Connexion impossible")
		log("ERROR", "ad", "Arrêt du programme")
		return sys.exit()



# Fonction recup_utilisateurs_actifs
#
# Récupère la liste des utilisateurs AD actifs
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @return list - Liste des utilisateurs actifs de l'AD
#
def recup_utilisateurs_actifs(cfg):
        """ Fonction chargée de récupérer les utilisateurs inactifs de l'AD"""
        # Definition des parametres necessaires de connexion AD
        ad_host = cfg.get('AD', 'ad_host')
        ad_login = cfg.get('AD', 'ad_login')
        ad_password = cfg.get('AD', 'ad_password')
        ad_dir_enabled_users = cfg.get('AD', 'ad_dir_enabled_users')
        ad_filter_en = cfg.get('AD', 'ad_filter_en')
        ad_user = cfg.get('AD', 'ad_user')
        ad_alias = cfg.get('AD', 'ad_alias')
	ad_domain = cfg.get('AD', 'ad_domain')
        # Definition des methodes de connexion sur l'AD
        server =  Server(ad_host, get_info=ALL)
        conn_server = Connection(server, ad_login, ad_password, auto_bind=True)
        # Definition du filtre de recherche sur l'AD
        attrs = [ad_user, ad_alias]
        conn_server.search(ad_dir_enabled_users, ad_filter_en, attributes = attrs)
	# Creation d'un dictionnaire vierge
        enabled_users = {}
        # Parcourt des lignes de chaque compte récupérés dans l'AD
        for row in conn_server.entries:
                # Si Attribut de l'AD present dans la ligne
                if ad_alias in row :
			# Creation d'une variable "mail et alias_mail"
			mail = ('%s%s' % (row[ad_user], ad_domain))
			alias_mail = ('%s' % (row[ad_alias]))
                        # Ajout de l'alias mail en tant que valeur à la clef mail dans le dictionnaire "enabled_users"
			enabled_users[mail] = alias_mail
        # On retourne le dictionnaire
	return enabled_users


