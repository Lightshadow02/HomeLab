# Scripts

[← Retour au README](../README.md)

| Script | Où il tourne | Rôle |
|---|---|---|
| [inventaire.sh](inventaire.sh) | Hôte Proxmox | Inventaire **en lecture seule** : matériel, stockage, réseau, invités, sauvegardes, état de sécurité. A servi à produire cette documentation |
| [wait-nas-mounts.sh](wait-nas-mounts.sh) | Hôte Proxmox (au démarrage) | Attend que les montages NFS soient prêts (5 min max.) avant de démarrer les invités qui les utilisent |
| [pbs-grid.py](pbs-grid.py) | Cron, toutes les 10 min | Lit l'historique des tâches PBS via un relais en lecture seule et calcule la grille des sauvegardes sur 30 jours pour le tableau de bord |
| [jf-pause-stop.py](jf-pause-stop.py) | Cron, toutes les 30 min | Coupe les lectures Jellyfin en pause depuis plus de 2 h (arrêt de la lecture, arrêt du transcodage, ou déconnexion après 6 h pour les clients non pilotables) |

Bonnes pratiques appliquées :
- un mode `--dry-run` pour tout script qui modifie quelque chose ;
- les jetons et clés sont lus dans des **fichiers protégés** (`chmod 600`), jamais écrits dans le code ;
- des jetons API à **privilèges minimaux** (lecture seule quand c'est possible) ;
- des écritures atomiques (fichier temporaire, puis `os.replace`) pour ne jamais servir un fichier à moitié écrit.
