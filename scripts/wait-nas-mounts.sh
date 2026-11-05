#!/bin/sh
# Wait (max 5 min) for the NAS NFS mounts before Proxmox starts guests that bind-mount them.
for i in $(seq 1 60); do
  ok=1
  for m in /mnt/nas-media/film /mnt/nas-media/serie /mnt/nas-media/anime /mnt/nas-media/scan /mnt/nextcloud-data /mnt/pbs-datastore; do
    mountpoint -q "$m" || { mount "$m" 2>/dev/null; ok=0; }
  done
  [ $ok = 1 ] && { echo "NAS mounts ready"; exit 0; }
  sleep 5
done
echo "NAS mounts not ready after 5 min, starting guests anyway" >&2
exit 0
