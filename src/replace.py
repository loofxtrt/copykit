from pathlib import Path

def replace(search_term: str, substitute_file: Path, target_dir: Path):
    for f in target_dir.iterdir():
        pass