#!/usr/bin/bash

set -e

/usr/lib/plasma-changeicons Papirus

python3 -m src.copykit -r local

/usr/lib/plasma-changeicons copycat