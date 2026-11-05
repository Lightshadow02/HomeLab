# 02 — Proxmox VE

[← Retour au README](../README.md)

## Version et mode

| Élément | Valeur |
|---|---|
| Version | **Proxmox VE 9.2** (pve-manager 9.2.21), Debian 13 « trixie » |
| Noyau | 7.0 (proxmox-kernel) |
| Topologie | **Nœud unique**, pas de cluster |
| Dépôts | `pve-no-subscription` + dépôts Debian officiels (dépôts enterprise désactivés) |

### Pourquoi Proxmox ?

- **Gratuit**, sans limite fonctionnelle, et **très solide** en production.
- VM (KVM) et conteneurs (LXC) dans la même interface.
- Sauvegarde native avec **Proxmox Backup Server** : déduplication, vérification, rétention.
- API complète, utilisée pour la supervision (exporter Prometheus) et pour les scripts.

## Stockage

| ID Proxmox | Type | Support | Contenu | Utilisation |
|---|---|---|---|---|
| `local` | dir | NVMe (LV root, 96 Go) | ISO, modèles | 14 % |
| `local-lvm` | **LVM-thin** | NVMe (1,67 To) | Disques des VM et CT | 41 % |
| `HDD-2TO` | dir | HDD 2 To | Sauvegardes vzdump, datastore PBS secondaire | 20 % |
| `backup` | dir (point de montage NFS) | Buffalo TeraStation | Anciennes sauvegardes vzdump | 11 % |
| `pbs-buffalo` | **pbs** | CT 107 → Buffalo | Sauvegardes quotidiennes | 6 % |

### Pourquoi LVM-thin plutôt que ZFS ?

L'hôte n'a qu'**un seul disque rapide** : ZFS n'apporterait pas de redondance, et consommerait beaucoup de RAM (ARC) pour un gain limité.
LVM-thin permet le **provisionnement fin** et les **snapshots**, ce qui suffit pour les sauvegardes en mode `snapshot` et pour revenir en arrière avant une mise à jour risquée.

### Montages NFS de l'hôte

Les NAS sont montés **sur l'hôte**, puis transmis aux conteneurs par des **points de montage** (`mpX`), éventuellement en lecture seule :

```text
NAS médias  ──NFS──▶ /mnt/nas-media/{film,serie,anime,scan} ──mp ro──▶ CT Jellyfin
Buffalo     ──NFS──▶ /mnt/nextcloud-data                     ──mp────▶ CT Nextcloud
Buffalo     ──NFS──▶ /mnt/LABO-BACKUP/…/pbs-datastore.raw  ──loop──▶ /mnt/pbs-datastore ──mp──▶ CT PBS
```

Pourquoi ce schéma :
- les conteneurs **non privilégiés** ne peuvent pas monter de NFS eux-mêmes, et ils n'ont pas à le faire ;
- l'accès au stockage reste **centralisé et contrôlé** depuis l'hôte, avec la lecture seule là où c'est possible.

Un script `wait-nas-mounts` fait attendre le démarrage des invités jusqu'à ce que les montages NFS soient prêts, avec un maximum de 5 min. Sans lui, un conteneur pourrait démarrer sur un dossier vide après une coupure.
Voir [configs/proxmox/](../configs/proxmox/).

## Réseau de l'hôte

| Bridge | Port physique | Rôle |
|---|---|---|
| `vmbr0` | nic0 | WAN : relie pfSense à la box. L'hôte y a son IP d'administration |
| `vmbr1` | aucun | LAN **purement virtuel** derrière pfSense |
| `vmbr200` | aucun | Zone isolée « Cloud » (Nextcloud) |
| `vmbr999` | nic1 | Réseau de stockage vers les NAS |

Tous les bridges sont configurés avec `bridge-stp off` et `bridge-fd 0`. Le fichier complet, nettoyé, est dans [configs/proxmox/interfaces](../configs/proxmox/interfaces).

## Conventions

| Plage d'ID | Usage |
|---|---|
| `100` | Routeur / pare-feu |
| `101–107` | Services d'infrastructure (proxy, supervision, médias, cloud, bureau, sauvegarde) |
| `2xx` | Sites web |
| `600` | Téléphonie |
| `99x` | Outils d'administration et machines de test |

- Hostnames en majuscules pour les rôles d'infrastructure (`PBS`, `NEXTCLOUD`, `BUREAU`).
- **Démarrage automatique** (`onboot`) sur tous les services de production. PBS démarre en 2e position, après pfSense.
- Une machine de **test** temporaire, créée par clonage d'une sauvegarde, sert à répéter les mises à jour risquées avant la production. Voir [08 — Historique](08-historique.md).
- Avant chaque intervention lourde, je prends un **snapshot** nommé avec la date (exemple : `preupgrade_AAAAMMJJ`).

## Pourquoi des conteneurs LXC + Docker plutôt que des VM ?

> « Les conteneurs, c'est bien mieux que les VM pour la sécurité, l'optimisation de la place et les performances. »

- **Performances** : pas d'émulation matérielle, et accès quasi natif au CPU et aux disques.
- **Place** : un conteneur Debian occupe quelques centaines de Mo, contre plusieurs Go pour une VM.
- **Sécurité** : tous les LXC sont **non privilégiés**. Le root du conteneur est mappé sur un utilisateur sans droits de l'hôte (UID 100000+), et Docker tourne à l'intérieur avec `nesting`.
- Les **VM** sont réservées à ce qui l'exige : **pfSense**, qui est sous FreeBSD et a besoin de ses propres cartes réseau, et l'**IPBX**.
