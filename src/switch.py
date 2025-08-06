import os
from pathlib import Path
from shutil import copy2

from src.utils import logger

def switch(target_dir: Path, source_dir: Path):
    """
        faz com que todos os ícones de um pack (target_dir)  
        sejam substituídos pelos ícones que o source_dir tem com o mesmo nome  
        por segurança, não faz busca recursiva, e só afeta os itens especificamente do dir indicado
    """

    if not target_dir.exists():
        return

    # passar todos os nomes de arquivo do source_dir pra um dicionário
    # se usa um dict ao invés de uma list pra que se possa usar o .get("file_name")
    # assim, o nome do arquivo é a chave, e o valor da chave é o próprio arquivo
    source_dir = {f.name: f for f in source_dir.iterdir() if f.is_file()}

    for icon in target_dir.iterdir():
        if not icon.is_file():
            continue

        # ignorar arquivos que são links simbólicos
        if os.path.islink(icon):
            continue

        twin = source_dir.get(icon.name)

        if twin:
            copy2(twin, icon)
            logger.success(f"{icon.name} substituído")
        else:
            logger.info(f"o diretório de entrada não possui o arquivo {icon.name}; ignorando")