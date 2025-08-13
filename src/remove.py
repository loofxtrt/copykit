from pathlib import Path

from src.utils import logger

def remove(icon_path: Path):
    if icon_path.is_symlink():
        logger.debug("symlink: o arquivo pra remoção é um symlink")
    else:
        logger.debug("comum: o arquivo pra remoção é um arquivo comum")
    
    icon_path.unlink(missing_ok=True)
    logger.remove(f"arquivo removido: {icon_path}")