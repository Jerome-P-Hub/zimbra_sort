#!/usr/bin/python
# -*- coding: utf-8 -*-



"""Ce fichier execute les actions necessaires au tri des utilisateurs n'étant plus présents dans Zimbra 


Il s'appuie sur les fichiers :
- ad.py
- zimbra.py """


import sys
import logs
from ad import *
from zimbra import *
from archiv import *
from alias import *
import ConfigParser
import datetime




# Test a blanc
dryrun = False




# on effectue la lecture des donnees contenues dans le fichier conf.ini
cfg = ConfigParser.ConfigParser()
cfg.read('/scripts/conf.ini')

date = datetime.datetime.now()
logs.logPath = "%s%s%s%s" % (cfg.get('LOG','logDir'), cfg.get('LOG','logFile'), "%s%s%s" % (date.year,'{:02d}'.format(date.month),'{:02d}'.format(date.day)), cfg.get('LOG','logFileExt'))





""" On récupère les fonctions necessaires dans des listes """

log ("INFO", "sort", "Début de Logs")
	
palliatif_utilisateurs_zimbra = palliatif_recup_utilisateurs(cfg)
recup_precedents_utilisateurs = recup_precedents_utilisateurs(cfg, palliatif_utilisateurs_zimbra)
utilisateurs_ad_desactives = recup_utilisateurs_inactifs(cfg)
utilisateurs_zimbra = recup_utilisateurs(cfg)
liste_nouveaux = liste_nouveaux(recup_precedents_utilisateurs, utilisateurs_zimbra)
ajout_archive = ajout_archive(cfg, liste_nouveaux, dryrun)
utilisateurs_zimbra_a_desactiver = recup_zimbra_utilisateurs_a_desactiver(utilisateurs_ad_desactives, utilisateurs_zimbra)
desactivation_zimbra_utilisateur = desactivation_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)
archivage_zimbra_utilisateur = archivage_utilisateur_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)
list_tmp_archivage = list_tmp_archivage(cfg, utilisateurs_zimbra_a_desactiver, dryrun)
suppression_archive_local = suppr_tmp_archivage(list_tmp_archivage, dryrun)
Copie_archives_vers_lecteur = copy_tmp_archivage(cfg, dryrun)
liste_archivage = list_archivage(cfg, dryrun)
suppression_archivage = suppr_archivage(liste_archivage, dryrun)
suppression_zimbra_utilisateur = suppression_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)
utilisateurs_ad_actifs = recup_utilisateurs_actifs(cfg)
utilisateurs_alias = recup_alias(cfg)
creation_alias = creation_alias(cfg, utilisateurs_ad_actifs, utilisateurs_alias, dryrun)

log ("INFO", "sort", "Fin de Logs \n")
