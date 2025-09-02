from pathlib import Path
from shutil import copy2

from src.utils import logger

def create(target_path: Path, file_to_create: Path, as_symlink_to: Path = None):
    """
        copia um arquivo de ícone pra um lugar onde originalmente ele NÃO existe  
        serve pra criar ícones em locais específicos, e não faz isso recursivamente  
        o target_path deve ser passado inteiro, incluindo o nome final do ícone  
        ex: */apps/scalable/btop.svg ao invés de só */apps/scalable/
    """

    # variações do mesmo icon pack podem dar erro por não terem a mesma estrutura,
    # foca só nos dirs que existem
    if not target_path.parent.exists():
        return

    # ignorar arquivos já criados
    if target_path.exists():
        return

    if not str(target_path).endswith(".svg"):
        target_path = Path(str(target_path) + ".svg")

    if as_symlink_to is not None:
        target_path.symlink_to(as_symlink_to)
        logger.create(f"symlink criado: {target_path} -> {as_symlink_to}")
    else:
        copy2(file_to_create, target_path)
        logger.create(f"arquivo criado: {target_path}")