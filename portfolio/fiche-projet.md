# Fiche projet — HomeLab Proxmox (textes pour le portfolio)

Textes prêts à copier-coller sur [hloureiro.fr](https://hloureiro.fr). Toutes les informations viennent de la documentation du dépôt.

---

## Titre
**HomeLab — Infrastructure virtualisée et sécurisée sous Proxmox VE**

## Accroche (1 ligne)
Une infrastructure de type PME sur un seul serveur : pare-feu et IPS, zones réseau, VPN, supervision et sauvegardes vérifiées.

## Résumé court (≈ 50 mots)
Mon laboratoire personnel tourne 24 h/24 sur un serveur Ryzen 9 (96 Go de RAM) sous Proxmox VE.
Il réunit un pare-feu pfSense avec IPS Snort et filtrage DNS, des zones réseau séparées, un VPN WireGuard, un reverse proxy TLS,
une supervision Prometheus, Grafana et Loki avec des alertes, et des sauvegardes Proxmox Backup Server vérifiées.

## Description longue (≈ 180 mots)
Depuis ma première année de BTS (2021), je fais évoluer chaque année un laboratoire personnel : d'un Raspberry Pi à un serveur Ryzen 9 sous Proxmox VE.
Il héberge aujourd'hui des services utilisés au quotidien (cloud privé, visioconférence, serveur multimédia, téléphonie IP), avec une approche **défense en profondeur** :

- **Périmètre** : pfSense virtualisé, refus par défaut, IPS **Snort** en blocage sur le WAN, **pfBlockerNG** (≈ 352 000 domaines malveillants ou publicitaires bloqués).
- **Segmentation** : le cloud exposé est isolé dans sa propre zone, et le stockage est sur une interface physique dédiée.
- **Accès** : VPN **WireGuard**. Les consoles d'administration ne sont jamais exposées : reverse proxy TLS et listes d'accès.
- **DNS et TLS** : DNS local *split-horizon* avec validation DNSSEC (les consoles internes n'existent pas dans le DNS public), certificats **Let's Encrypt** ECDSA, avec un wildcard obtenu par challenge DNS.
- **Supervision** : Prometheus, Grafana et Loki. Les journaux du pare-feu sont centralisés, et les alertes, rédigées en français, arrivent sur téléphone.
- **Sauvegardes** : Proxmox Backup Server, avec 2 copies, une vérification hebdomadaire et une restauration testée.

Le dépôt documente l'architecture, les choix techniques, les incidents rencontrés et les leçons que j'en ai tirées.

## Chiffres clés
| | |
|---|---|
| Serveur | Ryzen 9 5900X · 24 threads · 96 Go RAM |
| Invités | 2 VM et 7 conteneurs LXC en service |
| Conteneurs Docker | plus de 35 |
| Règles pare-feu | 121 |
| Domaines bloqués (DNSBL) | ≈ 352 000 |
| Connexions malveillantes bloquées | ≈ 100 000 par jour (≈ 900 adresses) |
| Stockage réseau | 22 To + 11,6 To |

## Technologies (étiquettes)
`Proxmox VE` `pfSense` `Snort` `pfBlockerNG` `WireGuard` `Docker` `LXC` `Nginx Proxy Manager` `Let's Encrypt`
`Prometheus` `Grafana` `Loki` `Proxmox Backup Server` `Nextcloud` `Asterisk` `Frigate` `OpenVINO` `NFS` `Python` `Bash`

## Compétences démontrées
Sécurité réseau · Détection d'intrusion (IPS) · Journalisation centralisée · Virtualisation · Conteneurisation ·
Sauvegarde et restauration · Supervision et alerting · Gestion des vulnérabilités · Automatisation (scripts Python et Bash)

## Liens
- Dépôt : https://github.com/Lightshadow02/HomeLab
- Projet associé : https://github.com/Lightshadow02/baszel-snmp-bridge
- Page autonome : [homelab.html](homelab.html)
- Données : [homelab.json](homelab.json)

## Images
| Fichier | Légende proposée |
|---|---|
| `assets/grafana-hote.png` | Supervision de l'hôte Proxmox dans Grafana |
| `assets/grafana-pfblockerng.png` | pfBlockerNG : 100 000 connexions malveillantes bloquées en 24 h |
| `assets/pbs-sauvegardes.png` | Sauvegardes Proxmox Backup Server sur 30 jours |

Lien direct vers une image (à utiliser sur le site) :
`https://raw.githubusercontent.com/Lightshadow02/HomeLab/main/assets/grafana-hote.png`
