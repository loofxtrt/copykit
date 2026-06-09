from pathlib import Path
import shutil

from ..models import Target, Entry, Context
from ..logger import EntryLogger
from ..utils import is_icon_valid
from .. import processor
# from .. import logger, processor


def handle_create_or_replace(
    entry: Entry,
    target: Target,
    context: Context,
    hard_replace: bool,
    skip_symlinks: bool,
    logger: EntryLogger
    ):
    """
    lida com ações de criação ou substituição de arquivos a partir de um substituto

    args:
    	entry:
    		entry que contém o substituto e os targets associados

    	target:
    		target atual que define o caminho e a ação a ser executada

    	hard_replace:
    		define se a substituição deve ignorar validações do destino

    	skip_symlinks:
    		define se symlinks devem ser ignorados durante replace
    """
    
    # garantir que existe um substituto válido antes de qualquer operação
    substitute = entry.substitute
    if not substitute:
        logger.error(f'substituto não encontrado para {target.icon}')
        return
    
    substitute_path = substitute.resolve_path(context)
    if not is_icon_valid(substitute_path):
        logger.error(f'caminho de substituto inválido: {substitute_path}')
        return

    # resolver o target
    target_path = target.resolve_path(context)
    
    # após ter um caminho de ícone substituto válido, as ações podem começar
    if target.action == 'replace':
        if not hard_replace:
            if not is_icon_valid(target_path):
                logger.error(f'caminho de target inválido: {target_path}')
                return

            if target_path.is_symlink() and skip_symlinks:
                logger.info(f'symlink pulado: {target.icon}')
                return
    
        _copy(substitute=substitute_path, destination=target_path, operation='substituído', logger=logger)
    elif target.action == 'create':
        _copy(substitute=substitute_path, destination=target_path, operation='criado', logger=logger)

    # aplicar processing
    if entry.processing:
        processor.run(
            processing_id=entry.processing,
            svg=target_path,
            dest=target_path
        )

# TODO: param (flag) pra chamar ou não o processor e otimizar os svgs ao copiar eles
# TODO: param pra ensure_parents?
def _copy(
    substitute: Path,
    destination: Path,
    operation: str,
    logger: EntryLogger
    ):
    """
    copia um arquivo substituto para o destino, removendo qualquer arquivo existente antes

    args:
    	substitute:
    		caminho do arquivo que será copiado

    	destination:
    		caminho onde o arquivo será colocado. isso já inclui o nome do arquivo
            não é só o parent de onde ele deve estar

    	operation:
    	    descrição textual da operação para logging. ex: 'criado', 'substituído'
    """

    try:
        # limpar o destino, removendo o alvo antes de substituir ele
        if destination.exists() or destination.is_symlink():
            try:
                destination.unlink()
            except Exception as err:
                logger.error(f'erro ao deletar {destination} para substituí-lo com {substitute}')
                logger.error(err)

        shutil.copy2(substitute, destination)
        logger.success(f'arquivo {operation}: {destination}')
    except Exception as err:
        logger.error(f'erro ao copiar o substituto {substitute} para {destination}')
        logger.error(err)