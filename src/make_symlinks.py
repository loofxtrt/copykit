from src.utils import logger

from pathlib import Path

def make_symlinks(original_file: Path, new_symlink: Path):
    # referenciar apenas relativamente, nao fazer o symlink ser hardcoded
    original_file = original_file.name

    if new_symlink.is_symlink() or new_symlink.exists():
        return

    new_symlink.symlink_to(original_file)
    logger.success("symlink criado")