from pathlib import Path
from shutil import copy2

from src.utils import logger

def create(target_path: Path, file_to_create: Path):
    """
        copia um arquivo de ícone pra um lugar onde originalmente ele NÃO existe  
        serve pra criar ícones em locais específicos, e não faz isso recursivamente  
        o target_path deve ser passado inteiro, incluindo o nome final do ícone  
        ex: */apps/scalable/btop.svg ao invés de só */apps/scalable/
    """
    
    if not target_path.parent.exists():
        return

    copy2(file_to_create, target_path)
    logger.create(f"arquivo criado: {target_path}")