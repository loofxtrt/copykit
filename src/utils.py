from pathlib import Path
import shutil
import json
import tomllib


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

def write_json(file: Path, data: dict) -> dict:
    with file.open('w', encoding='utf-8') as f:
        return json.dump(data, f, indent=4, ensure_ascii=False)

def read_toml(file: Path) -> dict:
    with file.open('rb') as f:
        return tomllib.load(f)

def is_icon_valid(file: Path) -> bool:
    return file.is_file() and file.suffix == '.svg'

def drop_empty(data: dict) -> dict:
    """
    filtra um dict, removendo todos os valores vazios dele
    isso inclui nulos, listas vazias, strings vazias etc.
    mas não inclui 0, false etc.
    """

    return {
        k: v for k, v in data.items()
        if v is not None and v != [] and v != '' and v != {}
    }

def safe_delete(path: Path):
    # IMPORTANTE
    # is_symlink, mesmo possivelmente apontando pra um diretório,
    # ainda é tratado como arquivo, pq é um link pra um dir, não um dir em si
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()

    # TODO: raise exception 