from pathlib import Path
from shutil import copy2

from src.utils import logger

def replace(target_names: list, substitute_file: Path, destinations_dirs: list[Path], force_hard_replace: bool = False):
    """
        target_name: lista com o nome EXATO dos arquivos que devem ser substituídos. deve ser exato porque se não, nomes como "obs" e "obsidian"  
        seriam ambíguos por ambos terem "obs" presente no nome. deve incluir extensão, como .svg
          
        substitute_file: o path completo do arquivo pelo qual o alvo será substituídos
          
        destinations_dirs: lista de paths de diretórios onde a busca será feita.  
        todos os arquivos dentro desse diretório que baterem com o nome do target vão ser substituídos  
        é uma lista pra que diferentes versões do mesmo icon pack possam ser mudadas em uma chamada. ex: kora-light, kora-dark  
          
        force_hard_replace: se estiver como true, vai substituir os symlinks por uma cópia real, ao invés de pular eles
    """

    if not substitute_file.is_file():
        logger.error(f"o arquivo substituto {substitute_file} é inválido")
        return
    
    logger.info("iniciando substituição")

    for destination in destinations_dirs:
        if not destination.exists() or not destination.is_dir():
            logger.error(f"o diretório alvo {destination} não existe ou é inválido")
            continue

        # substituir os arquivos que têm o nome de cada target com o substituto
        for trg_name in target_names:
            # adicionar .svg no final do nome do alvo caso já não tenha
            if not trg_name.endswith(".svg"):
                trg_name += ".svg"

            for f in destination.rglob("*"): # rglob ao invés de iterdir pra que a busca seja recursiva
                # pular symlinks conforme a flag
                if not force_hard_replace and f.is_symlink:
                    continue
                
                if f.name == trg_name:
                    try:
                        copy2(substitute_file, f)
                        logger.success(f"arquivo substituído: {f}")
                    except Exception as err:
                        logger.error(f"erro ao substituir {f}: {err}")