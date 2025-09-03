#!/usr/bin/bash

# reseta o icon pack local pra versão estável do repositório
cd /mnt/seagate/symlinks/kde-user-icons
sudo rm -rf /mnt/seagate/symlinks/kde-user-icons/copycat
cp -r /mnt/seagate/symlinks/copycat-repo/copycat/ ./copycat