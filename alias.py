#!/usr/bin/python
# -*- coding: utf-8 -*-



"""
alias.py

Ce script detecte les utilisiteurs zimbnra qui ne possède pas d'alias et en crée un automatiquement.


Author: Jerome Plewa
Version: 1.0
Date: 01/2021

Il charge et utilise le fichier conf.ini contenant les differents parametres obligatoires
"""






from ldap3 import Server, Connection, ALL
import os
import sys
import string
import datetime
import csv
from logs import *


#
# Fonction creation_alias
#
# Détecte et créé les alias manquants dans zimbra en comparant un dictionnaire des utilisateurs AD avec leur alias et un dictionnaire tiré de zimbra avec les email et leur alias
#
# @param cfg - Objet ConfigParser contenant les paramètres globaux du script
# @param utilisateurs_ad_actifs - Dictionnaire provenant du module "ad.py" contenant les utilisateurs présents dans l'AD associé à leur alias connu 
# @param utilisateurs_alias - Dictionnaire provenant du module "zimbra.py" contenant les utilisateurs zimbra présents associé à leur alias, si déjà créé 
# @param dryrun - Booleen dryrun, si vrai l'execution des commandes système ne se fera pas 
# @return
#
def creation_alias(cfg, utilisateurs_ad_actifs, utilisateurs_alias, dryrun):
	# Definition des parametres necessaires
	ad_domain = cfg.get('AD', 'ad_domain')
	zcmd_add_user_alias = cfg.get('ZIMBRA', 'zcmd_add_user_alias')
	ad_users = utilisateurs_ad_actifs
	zimbra_users = utilisateurs_alias
	# creation d'une liste alias_zimbra contenant les alias a créer
	alias_zimbra = []
	# Pour chaque items du dictionnaire "zimbra_users", on associe value à key => key : value
	for key_zimbra, value_zimbra in zimbra_users.items():
		key_zimbra = key_zimbra.rstrip()
		value_zimbra = value_zimbra.rstrip()
		# Si la valeur correspond à "[]" alors:
		if value_zimbra == "[]":
			# Pour chaque items du dictionnaire "ad_users", on associe value2 à key2 => key2 : value2
			for key_ad, value_ad in ad_users.items():
				key_ad = key_ad.rstrip()
				value_ad = value_ad.rstrip()
				# Si key2 correspond à key alors
				if key_ad == key_zimbra:
					# Si ad_domain compris dans value2 alors
					if ad_domain in value_ad:
						# Ajout de cette valeur a la liste alias_zimbra
						alias_zimbra.append(value_ad)
						# Log de l'information 
						log("INFO", "alias", "Utilisateur Zimbra nécessitant la création d'un alias: %s" % (value_ad))
						# Définition d'une variable "creation_user_alias" contenant la commande à utiliser sur zimbra pour créer l'alias
						creation_user_alias = zcmd_add_user_alias % (key_zimbra, value_ad)
						#  Verification du boolen dryrun puis execution de la commande si dryrun défini sur false
						if not dryrun:
							# Creation de l'alias
        		                                os.system(creation_user_alias)
							#log de la creation de l'alias
							log("INFO", "alias", "Alias Zimbra %s créé" % (value_ad))
	return	





