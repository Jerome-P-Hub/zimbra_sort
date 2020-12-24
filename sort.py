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
dryrun = False

# on effectue la lecture des donnees contenues dans le fichier conf.ini
cfg = ConfigParser.ConfigParser()
cfg.read('/scripts/conf.ini')



""" On récupère les fonctions necessaires dans des listes """

recup_precedents_utilisateurs = recup_precedents_utilisateurs_(cfg)

utilisateurs_ad_desactives = recup_utilisateurs_inactifs(cfg)

utilisateurs_zimbra = recup_utilisateurs(cfg)

utilisateurs_zimbra_a_desactiver = recup_zimbra_utilisateurs_a_desactiver(cfg, utilisateurs_ad_desactives, utilisateurs_zimbra)

desactivation_zimbra_utilisateur = desactivation_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

archivage_zimbra_utilisateur = archivage_utilisateur_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

list_tmp_archivage = list_tmp_archivage(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

suppression_archive_local = suppr_tmp_archivage(list_tmp_archivage, dryrun)

Copie_archives_vers_lecteur = copy_tmp_archivage(cfg, dryrun)

liste_archivage = list_archivage(cfg, dryrun)

suppression_archivage = suppr_archivage(liste_archivage, dryrun)

suppression_zimbra_utilisateur = suppression_utilisateurs_zimbra(cfg, utilisateurs_zimbra_a_desactiver, dryrun)

liste_nouveaux = liste_nouveaux(recup_precedents_utilisateurs, utilisateurs_zimbra)

ajout_archive = ajout_archive(cfg, liste_nouveaux, dryrun)





