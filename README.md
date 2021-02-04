# Zimbra-Sort

L'objectif premier de ce script est de tourner au plus près des utilisateurs actifs (présents) dans l'organistation afin d'économiser les licenses requises embarquées sur un serveur Zimbra Collaboration Network Edition et d'ainsi réduire les coûts d'acquisition des licences. Cela inclut des économies de temps passés à faire ces manipulations au quotidien, ce qui peut vite devenir redondant et chronophage dans une entreprise il y a beaucoup de turn-over et/ou il y a beaucoup d'utilisateurs finaux de la messagerie.
 <br>     Le second objectif est de stocker les BAL archivées sur du stockage à faible coût permettant ainsi d'économiser de l'espace sur votre baie à haut rendement incluant de haut coûts d'investissement et de maintenance. Cela permet donc de sauvegarder les BAL sur du stockage froid tel un NAS.
  <br>     Un des autres objectifs du script est de créer un alias automatiquement en fonction de vos besoins, cela impose le prérequis d'embarquer dans son AD l'attribut userPrincipalName renseigné au préalable par l'alias necessaire à créer dans ZImbra (module désactivable)
  <br>     Si vous pratiquez un nommage unique pour les utilisateurs présents chez vous, alors , lors de leur retour dans l'entreprise (turn-over), la précédente BAL sauvegardée est automatiquement uploader dans la BAL de l'utilisateur revenue et il bénéficie ainsi de l'accès à ces précédents mails. (désactivable également)



  <br> 
  <br> 
  
## Fonctionnement global:

Script Python appelant différents modules. 
  
    sort.py   -> Module principal, celui à exécuter
    ad.py     -> Module qui interroge votre AD ou Samba AD (Récupération de la liste des utilistauers inactifs de l'AD)
    zimbra.py -> Module qui récupère les utilisteurs actifs de Zimbra (Execute aussi des commandes spécifiques)
    archiv.py -> Module qui génère les archive de BAL des utilisateurs à sortir
    alias.py  -> Module qui génère un type d'alias particulier pour l'organisation (cette option peut ne pas être utilisé)
    logs.py   -> Module qui crée des logs entre les différentes étapes du script à des instants spécifiés (sauvegardés sous forme de fichier)
        
  <br> 
  <br> 
  
## Le fichier conf.ini:
  C'est ici qu'il faut définir les spécifités de votre organisation.
         
         Partie AD:
         YOUR_HOST: Le nom d'hôte DNS accessible de votre AD
         YOUR_PASSWORD: Le mot de passe "Administrator" ou autre compte capable d'interroger de votre AD
         YOUR_OU: L'OU spécifique des utilisateurs désactivés de votre AD, ici enregistrée sous l'OU people (Prérequis obigatoire)
         YOUR_DOMAIN: Votre nom de domaine exempté du .fr, défini ici par défaut, également à changer en fonction de votre FQDN. 
         @your_domain.fr: @votre_nom_de_domaine_de_messagerie.fr
         
         Partie ZIMBRA:
         YOUR_HOST_ZIMBRA: Le nom d'hôte DNS accessible de votre serveur Zimbra
         YOUR_PASSWORD_ZIMBRA: Le mot de passe "Zimbra" de votre serveur Zimbra
         YOUR_DOMAIN: Votre nom de domaine exempté du .fr, défini ici par défaut, également à changer en fonction de votre FQDN. 
         @YOUR_DOMAIN.fr: @votre_nom_de_domaine.fr
         /YOUR_DIR_LISTS/: Chemin de destination pour enregistrer les listes utilisateurs désactivés, supprimés, et recensés à J-1 (exemple: /scripts/lists/)
         
         Partie ARCHIVAGE:
         /YOUR_DIR_TMP_ARCHIV/: Chemin de destination pour enregistrer les BAL sauvegardés dans un dossier temporaire, régulé par un temp d'archivage (exemple: /scripts/archiv/)
         /YOUR_DIR_ARCHIV/: Chemin de destination pour copier les BAL sauvegardés du dossier temporaire vers un lecteur réseau externe, idéal pour sauvegarder dans le temps les                               BAL archivées. (exemple: /mnt/Zimbra_Archiv/)
         /YOUR_LISTS_DIR/YOUR_NAME_CSV_LIST.csv: Nom de fichier des agents désactivés dans chemin de destination (exemple: /scripts/lists/agents_desactives.csv
         archiv_tmp_dir_duration = 345600 -> par défaut 4 jours
         archiv_duration = 315360000 -> par défaut 10 ans
         
         Partie LOG:
         /YOUR_DIR_LOGS/: Chemin de destination pour enregistrer les LOGS (exemple: /scripts/logs/)



  <br> 
  <br> 

## Procédure de mise en place:
    
   Tout d'abord , déinifisser et inscriver dans le fichier conf.ini les prérequis nécessaires.
   Créer ensuite les différents répertoires necessaires de l'architecture,et y copier les differents scripts python et fichier conf.ini
                
              (Exemple: Créer /scripts/ et y copier les *.py et le fichier conf.ini
              Créer /scripts/lists/, /scripts/archiv/ et /scripts/logs/ )
             
 <br>
    
   Si le script des alias est non nécessaire, editer le fichier sort.py et ajouter un # en début de ligne  sur les 3 derniereres fonctions, de la sorte:
             
              #utilisateurs_ad_actifs = recup_utilisateurs_actifs(cfg)
              #utilisateurs_alias = recup_alias(cfg)
              #creation_alias = creation_alias(cfg, utilisateurs_ad_actifs, utilisateurs_alias, dryrun)
              
 <br>             
   Si le script de réintégration de la précédente BAL est non nécessaire, de la même manière, on commente les fonctions suivantes:
              
              #liste_nouveaux = liste_nouveaux(recup_precedents_utilisateurs, utilisateurs_zimbra)
              #ajout_archive = ajout_archive(cfg, liste_nouveaux, dryrun)






              



         
         
         
         
