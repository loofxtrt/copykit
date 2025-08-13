from pathlib import Path

def remove(icon_path: Path):
    icon_path.unlink(missing_ok=True)