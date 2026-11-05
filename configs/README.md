# Configurations (extraits nettoyés)

[← Retour au README](../README.md)

Les fichiers ci-dessous sont des **copies des fichiers réellement en production**, nettoyées avant publication :
- mots de passe, clés et jetons remplacés par `<REDACTED>` ;
- nom de domaine remplacé par `exemple.fr` ;
- machines non documentées retirées des listes.

| Dossier | Contenu |
|---|---|
| [proxmox/](proxmox/) | `interfaces` (bridges de l'hôte), montages NFS (`fstab-nas`) |
| [backup/](backup/) | Tâches de sauvegarde Proxmox VE et configuration de Proxmox Backup Server (rétention, synchronisation, vérification) |
| [monitoring/](monitoring/) | Pile de supervision : compose, Prometheus, Loki, Alloy (réception du syslog de pfSense) |
| [docker/](docker/) | Compose de Nextcloud, Nginx Proxy Manager, WireGuard (wg-easy), Jellyfin, Homarr, bureau KDE |

Les secrets de la supervision (`secrets/grafana.env`, `secrets/snmp.yml`, `secrets/pve.yml`) ne sont **pas** publiés :
le compose y fait référence, mais leur contenu reste sur le serveur.
