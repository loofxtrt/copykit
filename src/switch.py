from pathlib import Path
from shutil import copy2

from src.utils import logger

def switch(target_dir: Path, source_dir: Path):
    """
        faz com que todos os ícones de um pack (target_dir)  
        sejam substituídos pelos ícones que o source_dir tem com o mesmo nome  
        por segurança, não faz busca recursiva, e só afeta os itens especificamente do dir indicado
    """

    # passar todos os nomes de arquivo do source_dir pra um dicionário
    # se usa um dict ao invés de uma list pra que se possa usar o .get("file_name")
    # ao invés de ter que percorrer um array inteiro
    source_dir = {f.name for f in source_dir.iterdir() if f.is_file()}

    for icon in target_dir:
        if not icon.is_file():
            continue

        twin = source_dir.get(icon.name)

        if twin:
            copy2(src, trg)
        else:
            logger.info(f"o diretório de entrada não possui o arquivo {icon.name}; ignorando")