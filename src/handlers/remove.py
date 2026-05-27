from pathlib import Path

from ..models import Target
# from .. import logger


def handle_remove(
    target: Target,
    logger: EntryLogger
    ):
    """
    remove o arquivo ou symlink do target, se existir

    args:
    	target:
    		target que define o caminho do arquivo a ser removido
    """

    try:
        target.path.unlink()
        logger.success(f'{target.icon} deletado')
    except FileNotFoundError:
        logger.info(f'{target.icon} não precisa ser deletado porque já não existe')
    except Exception as err:
        logger.error(f'erro ao deletar {target.icon}')
        logger.error(err)