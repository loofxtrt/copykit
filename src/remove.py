from pathlib import Path

from src.utils import logger

def remove(icon_path: Path):
    icon_path.unlink(missing_ok=True)
    logger.remove(f"arquivo removido: {icon_path}")