#!/usr/bin/bash

# reseta o icon pack pro kora original (mas mantendo o index.theme como copycat)
cd /mnt/seagate/workspace/coding/projects/icons/copycat/
mv ./copycat ./copycat-tmp # guardar o anterior pra pegar o index dps
cp -r /mnt/seagate/symlinks/copykit-data/original-unzipped/kora/ ./copycat
cd ./copycat
rm -rf create-new-icon-theme.cache.sh icon-theme.cache index.theme
cp ../copycat-tmp/index.theme ./index.theme
rm -rf ../copycat-tmp