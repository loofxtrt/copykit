from pathlib import Path

from ..models import Target
from ..globals import normalize_svg_name
from .. import logger


def handle_symlink(canonical: Path, target: Target):
    """
    cria um symlink apontando para o arquivo master previamente definido

    args:
    	canonical:
    		caminho do arquivo que será referenciado pelo symlink

    	target:
    		target que define onde o symlink será criado
    """
    
    # symlink depende de um arquivo base previamente definido
    if not canonical:
        logger.error(f'erro ao criar o symlink. um canonical ainda não foi definido para {target.icon}')
        return
    
    # deletar o antigo arquivo/symlink que possivelmente existe no destino do symlink novo
    link = target.path
    if link.exists() or link.is_symlink():
        link.unlink()

    # criar o symlink
    canonical = normalize_svg_name(canonical)
    link.symlink_to(canonical)

    if not link.exists() or not link.is_file():
        logger.error(f'{link} não foi criado como um symlink válido')
        return

    logger.symlink(f'symlink {link} criado para {target.path}')