#!/usr/bin/bash

set -e

/usr/lib/plasma-changeicons Papirus

python3 -m src.copykit -e "/mnt/seagate/workspace/coding/projetos/scripts/copykit/environments/copyfax.qogir/environment.toml" apply -l local

/usr/lib/plasma-changeicons copyfax