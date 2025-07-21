from pathlib import Path
from shutil import copy2

from src.utils import logger

def replace(target_name: str, substitute_file: Path, destination_dir: Path):
    """
        target_name: o nome EXATO do arquivo que deve ser substituídos. deve ser exato porque se não, nomes como "obs" e "obsidian"  
        seriam ambíguos por ambos terem "obs" presente no nome  
        deve incluir extensão, como .svg
          
        substitute_file: o arquivo pelo qual o alvo será substituídos. também deve incluir extensão
          
        destination_dir: diretório onde a busca será feita. todos os arquivos dentro desse diretório que baterem com o nome do target  
        vão ser substituídos
    """
    
    if not destination_dir.exists() or not destination_dir.is_dir():
        logger.error(f"o diretório alvo {destination_dir} não existe ou é inválido")
        return

    if not substitute_file.is_file():
        logger.error(f"o arquivo substituto {substitute_file} é inválido")
        return

    # substituir os arquivos com o nome do target com o substituto
    count = 0
    for f in destination_dir.iterdir():
        if f.name == target_name:
            copy2(substitute_file, f)
            logger.info(f"arquivo substituídos: {f}")
            count += 1
    
    if count == 0:
        logger.info(f"nenhum arquivo chamado {target_name} foi encontrado em {destination_dir}")
    else:
        logger.success(f"{count} arquivos substituídos")