#!/bin/bash
# Inventaire en LECTURE SEULE d'un hôte Proxmox VE (aucune modification).
# Usage : ./inventaire.sh > inventaire-$(date +%F).txt   (en root sur l'hôte)
# Pensez à relire la sortie avant de la partager : elle peut contenir des noms internes.
set -u
section() { printf '\n===== %s =====\n' "$1"; }

section "Matériel"
cat /sys/class/dmi/id/board_vendor /sys/class/dmi/id/board_name 2>/dev/null
lscpu | grep -E 'Model name|^CPU\(s\)|Thread'
free -h | head -2
lsblk -d -o NAME,SIZE,MODEL,ROTA,TRAN | grep -v loop
lspci | grep -iE 'vga|ethernet|network'

section "Proxmox"
pveversion -v | head -3
pvesm status
lvs 2>/dev/null

section "Réseau de l'hôte"
grep -vE '^\s*#|^\s*$' /etc/network/interfaces

section "Invités"
qm list
pct list
for id in $(qm list | awk 'NR>1{print $1}'); do
  echo "--- VM $id"; qm config "$id" | grep -E '^(name|cores|memory|net[0-9]|scsi0|onboot)' | sed -E 's/=([0-9A-F]{2}:){5}[0-9A-F]{2}/=<MAC>/'
done
for id in $(pct list | awk 'NR>1{print $1}'); do
  echo "--- CT $id"; pct config "$id" | grep -E '^(hostname|cores|memory|rootfs|mp[0-9]|net[0-9]|onboot|unprivileged)' | sed -E 's/hwaddr=[^,]+,?//'
done

section "Sauvegardes"
cat /etc/pve/jobs.cfg

section "Sécurité de l'hôte"
sshd -T 2>/dev/null | grep -E '^(permitrootlogin|passwordauthentication|pubkeyauthentication) '
pve-firewall status
pveum user list
systemctl is-active fail2ban 2>/dev/null || true
ss -tlnp | awk 'NR>1{print $4}' | sort -u

section "Mises à jour en attente"
apt list --upgradable 2>/dev/null | tail -n +2 | wc -l
