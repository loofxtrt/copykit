#!/usr/bin/bash

# rm -rf /mnt/seagate/symlinks/kde-user-icons/copycat
# cp -r /mnt/seagate/symlinks/copycat/copycat /mnt/seagate/symlinks/kde-user-icons/copycat

set -e

SOURCE="/mnt/seagate/symlinks/copycat/copycat/"
TARGET="/mnt/seagate/symlinks/kde-user-icons/copycat/"

/usr/lib/plasma-changeicons Papirus

# copia só os arquivos que mudaram e não estão iguais
# ao estado atual do repositório original
rsync -a --delete --info=NAME "$SOURCE" "$TARGET"

/usr/lib/plasma-changeicons copycat