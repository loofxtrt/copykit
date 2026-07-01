from pathlib import Path

from ..models import Target, Context
from ..utils import normalize_svg_name, safe_delete
from ..logger import EntryLogger
from ..templates import resolve_placeholders
# from .. import logger


def handle_symlink(
    canonical: Path,
    target: Target,
    context: Context,
    logger: EntryLogger
    ):
    """
    cria um symlink apontando para o arquivo master previamente definido

    args:
    	canonical:
    		caminho do arquivo que será referenciado pelo symlink
            ex: 'blender.svg'

            ISSO NÃO NORMALIZA AUTOMATICAMENTE O NOME DO ARQUIVO,
            É EXIGIDO QUE ELE JÁ VENHA COM EXTENSÃO SE NECESSÁRIO

        context:
            contexto. pra saber como resolver o path do target

    	target:
    		target que define onde o symlink será criado
            ex: copycat/apps/scalable/blender-2.svg <- é um symlink
    """
    
    # symlink depende de um arquivo base previamente definido
    if not canonical:
        logger.error(f'erro ao criar o symlink. um canonical ainda não foi definido para {target.icon}')
        return
    
    # deletar o antigo arquivo/symlink que possivelmente existe no destino do symlink novo
    link = target.resolve_path(context)
    if link.exists() or link.is_symlink():
        safe_delete(link)
    
    if not link.parent:
        logger.error(f'parent inválido pro symlink {link}')
        return

    # criar o symlink    
    link.symlink_to(canonical)

    if not link.exists() and not link.is_symlink():
        safe_delete(link) # deleta o link quebrado que foi criado

        logger.error(f'{link} não foi criado como um symlink válido')
        return

    logger.symlink(f'criado symlink apontando para {canonical} -> {link}')

# TODO: try que cubra fileexistserror