# 09 — Roadmap

[← Retour au README](../README.md)

Légende : 🟢 en production · 🟡 en cours · ⚪ prévu

| État | Projet | Objectif |
|---|---|---|
| ⚪ | **SIEM** | Passer de la centralisation des journaux (Loki) à de la **détection** : collecte des journaux système de l'hôte et des conteneurs, règles de corrélation, tableau de bord type SOC |
| ⚪ | **SSO** | Authentification unique (OIDC) devant les consoles et les applications, et MFA centralisée |
| 🟡 | **Accélération GPU (NVENC)** | Transcodage Jellyfin par une carte NVIDIA plutôt que par le processeur. Carte de test à valider |
| ⚪ | **Copie de sauvegarde hors site** | Compléter la règle 3-2-1 (PBS distant ou synchronisation chiffrée) |
| ⚪ | **Segmentation plus fine** | Utiliser les bridges réservés pour séparer les services exposés (DMZ) de l'administration |
| ⚪ | **Filtrage GeoIP** | Restreindre l'exposition de la téléphonie aux pays attendus (pfBlockerNG) |
| 🟡 | **Durcissement continu** | Accès d'administration, mises à jour régulières, revue des comptes |

## Déjà réalisé (extrait)

- 🟢 Pare-feu et IPS virtualisés, DNSBL anti-malware et anti-phishing
- 🟢 Zone isolée pour le cloud exposé, réseau de stockage dédié
- 🟢 VPN WireGuard, reverse proxy TLS avec listes d'accès
- 🟢 Proxmox Backup Server, avec une seconde copie, vérification et restauration testée
- 🟢 Supervision Prometheus, Grafana et Loki, avec des alertes en français
