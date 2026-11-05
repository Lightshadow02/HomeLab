# 01 — Matériel

[← Retour au README](../README.md)

## Serveur principal

Machine **montée moi-même** sur une base de PC, utilisée 24 h/24 comme hyperviseur.

| Composant | Modèle | Remarques |
|---|---|---|
| Carte mère | Gigabyte **B550M AORUS ELITE** | Format micro-ATX, AM4 |
| Processeur | **AMD Ryzen 9 5900X** | 12 cœurs / 24 threads, virtualisation AMD-V |
| Mémoire | **96 Go DDR4** | 2 × 32 Go + 2 × 16 Go, 2133 MT/s |
| Disque système / VM | **Samsung 990 EVO 2 To** (NVMe) | Système Proxmox + pool LVM-thin des VM/CT |
| Disque secondaire | **Seagate Barracuda 2 To** (HDD SATA, ST2000DM008) | Sauvegardes locales (copie PBS, vzdump) |
| Réseau | Intel **I210** + Realtek **RTL8111** | 2 ports 1 GbE : un pour le WAN, un dédié au stockage |
| Carte graphique | NVIDIA GeForce **GT 710** | Affichage uniquement (pas d'encodage matériel) |

Températures relevées en fonctionnement : CPU **44 °C** (Tctl), NVMe **39 °C**.

## Choix du stockage

- **NVMe** pour les disques des machines : latence faible, indispensable avec une douzaine d'invités sur un seul disque.
- **HDD** pour les sauvegardes : capacité à bas coût. Il reçoit la **seconde copie** des sauvegardes PBS, pour limiter l'usure du NVMe.
- Les données volumineuses (médias, fichiers Nextcloud) ne sont **pas** sur le serveur : elles sont sur des NAS, montés en NFS.

## Stockage réseau

| Équipement | Rôle | Protocole | Capacité |
|---|---|---|---|
| **NAS médias** | Bibliothèque multimédia (films, séries, etc.) | NFS v4.1 | 22 To (rempli à 96 %) |
| **Buffalo TeraStation** | Sauvegardes (datastore PBS) + données Nextcloud | NFS v3 | 11,6 To |

Les deux NAS sont sur un **réseau de stockage séparé** (192.168.70.0/24), relié à une **carte réseau physique dédiée** du serveur.
Le trafic NFS ne passe donc ni par le pare-feu ni par le réseau des services. Voir [03 — Réseau](03-reseau.md).

## Consommation électrique

Non mesurée à ce jour.
