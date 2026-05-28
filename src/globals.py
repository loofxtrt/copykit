from pathlib import Path
import json


PACK_LOCAL = Path('/mnt/seagate/symlinks/kde-user-icons/copycat')
PACK_REMOTE = Path('/mnt/seagate/recursos/copycat/copycat') # icon pack dentro do repositório git
PACK_REPO = Path('/mnt/seagate/recursos/copycat') # repositório git
SUBSTITUTES = Path('/mnt/seagate/symlinks/copydb/substitutos')
INSTRUCTIONS = Path('/mnt/seagate/workspace/coding/projetos/scripts/copykit/instructions')


def _normalize_file_name(name: str, extension: str) -> str:
    if not extension.startswith('.'):
        extension = f'.{extension}'

    if not name.endswith(extension):
        name += extension

    return name

def normalize_svg_name(name: str) -> str:
    return _normalize_file_name(name, 'svg')

def normalize_json_name(name: str) -> str:
    return _normalize_file_name(name, 'json')

def read_json(file: Path) -> dict:
    with file.open('r', encoding='utf-8') as f:
        return json.load(f)