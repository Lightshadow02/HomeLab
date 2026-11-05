# 05 — Services

[← Retour au README](../README.md)

Une fiche par service, dans le même format : **rôle · hébergement · exposition · accès**.
Les fichiers de configuration nettoyés sont dans [configs/](../configs/).

---

## 🛡️ pfSense — routeur / pare-feu
| | |
|---|---|
| Rôle | Routage entre zones, NAT, pare-feu, IPS Snort, DNSBL, résolveur DNS |
| Hébergement | VM 100 (2 Go RAM) |
| Exposition | Interface WAN |
| Accès admin | LAN uniquement |

Voir [04 — Sécurité](04-securite.md).

## 🔀 Nginx Proxy Manager — reverse proxy TLS
| | |
|---|---|
| Rôle | Point d'entrée HTTPS unique, certificats Let's Encrypt, listes d'accès |
| Hébergement | CT 101 (Docker) |
| Exposition | 80/443 publiés |
| Accès admin | LAN/VPN |

Environ 21 hôtes virtuels, dont 14 réservés au LAN/VPN. Le reverse proxy injecte aussi un script dans l'interface de Jellyfin (voir plus bas).

## 🔐 WireGuard (wg-easy) — VPN
| | |
|---|---|
| Rôle | Accès distant à l'administration |
| Hébergement | CT 101 (Docker, réseau dédié 10.42.42.0/24) |
| Exposition | 51820/udp |
| Accès admin | interface web en LAN/VPN derrière le reverse proxy |

## ☁️ Nextcloud 34 — cloud privé et visio
| | |
|---|---|
| Rôle | Fichiers, agenda, Deck, visioconférence (Talk), tableau blanc |
| Hébergement | CT 105, **zone isolée OPT1** |
| Exposition | via reverse proxy + TURN pour la visio |
| Accès | comptes Nextcloud |

Pile Docker :

| Conteneur | Rôle |
|---|---|
| `nextcloud:34-apache` | Application (écoute uniquement sur l'IP de zone) |
| `mariadb:10.11` | Base de données, réseau interne |
| `redis:7` | Cache distribué + verrouillage de fichiers |
| `clamav` | Antivirus sur les fichiers déposés |
| `notify_push` | Notifications temps réel (moins de requêtes de synchronisation) |
| Talk **High-Performance Backend** (spreed + NATS + Janus) + **coturn** | Visio multi-participants, relais TURN |
| `whiteboard` | Tableau blanc collaboratif |

Optimisations réalisées :
- index de base de données manquants ajoutés ;
- cache distribué Redis ;
- génération des aperçus planifiée la nuit, avec une taille et une qualité limitées ;
- tâches de fond en **cron système** plutôt qu'en AJAX.

Les données (fichiers) sont sur le Buffalo en NFS, montées par l'hôte.

## 🎬 Jellyfin — serveur multimédia
| | |
|---|---|
| Rôle | Streaming de la bibliothèque (films, séries, animés) |
| Hébergement | CT 104 (Docker) |
| Exposition | via reverse proxy |
| Accès | comptes Jellyfin (une cinquantaine) |

- Bibliothèque montée en **lecture seule** depuis le NAS médias.
- **Badges VO / VF** : script maison injecté par le reverse proxy (`sub_filter` nginx) dans l'interface web et les applications.
  Il lit les pistes audio par l'API Jellyfin, et une étiquette Jellyfin permet de forcer le résultat à la main.
  Les en-têtes de cache sont neutralisés, pour que les applications ne gardent pas l'ancienne page en mémoire.
- **Sagas regroupées en dossiers** : script Python planifié chaque nuit. Il crée des collections Jellyfin à partir des sagas TMDB et de règles par mot-clé (145 collections), corrige les erreurs de rapprochement, et ne supprime jamais rien.
- **Coupure des lectures oubliées** : script planifié toutes les 30 min. Il arrête les lectures en pause depuis plus de 2 h, et libère le transcodage.
  Voir [scripts/jf-pause-stop.py](../scripts/jf-pause-stop.py).

## 📞 IPBX Asterisk — téléphonie IP
| | |
|---|---|
| Rôle | Standard téléphonique (SIP/RTP) |
| Hébergement | VM 600 |
| Exposition | SIP + plage RTP |
| Accès | — |

**Configuré entièrement à la main** (pas d'interface de type FreePBX).

## 🖥️ Bureau KDE à distance
| | |
|---|---|
| Rôle | Bureau Linux complet dans le navigateur, pour consulter les consoles internes depuis l'extérieur |
| Hébergement | CT 106 (Docker, image webtop) |
| Exposition | LAN/VPN uniquement |
| Accès | identifiant + mot de passe |

Remplace Guacamole : la personne se connecte au VPN, ouvre une URL, et obtient un bureau avec navigateur et client RDP/VNC/SSH.
Le DNS du conteneur est forcé sur pfSense, pour profiter du filtrage DNSBL et des noms internes.

## 💾 Proxmox Backup Server
Voir [06 — Sauvegardes](06-sauvegardes.md).

## 📊 Supervision — Prometheus, Grafana, Loki, Alloy
Voir [07 — Supervision](07-supervision.md).

## 🧭 Homarr — tableau de bord
| | |
|---|---|
| Rôle | Page d'accueil du lab : liens, état des services, widgets |
| Hébergement | CT 102 |
| Exposition | LAN/VPN |

Widget personnalisé : **grille des sauvegardes sur 30 jours**, « façon GitHub » (vert = OK, bleu = avertissement, rouge = erreur).
Ses données sont calculées par un script et servies par un **relais nginx en lecture seule** (jeton PBS limité au rôle *Audit*).
Voir [scripts/pbs-grid.py](../scripts/pbs-grid.py).

## 🐳 Arcane — gestion Docker
| | |
|---|---|
| Rôle | Gestion centralisée des conteneurs de tous les CT, notification des mises à jour d'images |
| Hébergement | gestionnaire sur CT 102 + **agent** dans chaque CT Docker |
| Exposition | LAN/VPN |

Remplace Portainer.

## 🎲 Applications web personnelles
| | |
|---|---|
| Rôle | Application de jeu de rôle (Node.js + PostgreSQL avec **sauvegarde automatique de la base**) et un hub de jeux web |
| Hébergement | CT 101 (Docker) |
| Exposition | via reverse proxy |

## 🛠️ Poste d'administration
| | |
|---|---|
| Rôle | Administration et automatisation (scripts, inventaire, assistant IA en ligne de commande) |
| Hébergement | CT 998 |
| Exposition | aucune |

---

### Services remplacés ou retirés

| Avant | Après | Raison |
|---|---|---|
| Portainer | **Arcane** | Gestion multi-hôtes par agents, notifications de mises à jour |
| Dashy | **Homarr** | Widgets dynamiques et intégrations |
| Beszel | **Prometheus + Grafana** | Logs centralisés + alerting avancé |
| Uptime Kuma | **blackbox-exporter + alertes Grafana** | Une seule pile de supervision |
| Guacamole | **Bureau KDE (webtop)** | Expérience complète, moins de briques |
| Partages SMB | **NFS** | Performances et fiabilité des montages |
