#!/usr/bin/python
# -*- coding: utf-8 -*-



"""Ce fichier execute les actions necessaires au tri des utilisateurs n'étant plus présents dans Zimbra 


Il s'appuie sur les fichiers :
- ad.py
- zimbra.py """



from ad import *
from zimbra import *
from archiv import *
import ConfigParser



# Test a blanc
dryrun = True

# on effectue la lecture des donnees contenues dans le fichier conf.ini
cfg = ConfigParser.ConfigParser()
cfg.read('/root/scripts/conf.ini')



""" On récupère les fonctions necessaires dans des listes """

utilisateurs_ad_desactives = recup_utilisateurs_inactifs(cfg)

utilisateurs_zimbra = recup_utilisateurs(cfg)

utilisateurs_zimbra_a_desactiver = recup_zimbra_utilisateurs_a_desactiver(cfg, utilisateurs_ad_desactives, utilisateurs_zimbra)

desactivation_zimbra_utilisateur = desactivation_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

archivage_zimbra_utilisateur = archivage_utilisateur_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

list_tmp_archivage = list_tmp_archivage(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

suppression_archive_local = suppr_tmp_archivage(list_tmp_archivage, dryrun)





""" Enregistrement de la liste des comptes Zimbra dans un fichier texte pour comparaison le lendemain"""
with open('liste_zimbra.txt', 'w') as liste_zimbra:
	liste_zimbra.write(str(utilisateurs_zimbra))




