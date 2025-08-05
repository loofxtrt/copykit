from pathlib import Path
from shutil import copy2

from src.utils import logger

def replace(target_names: list, substitute_file: Path, destinations_dirs: list[Path], force_creation_in: Path = None):
    """
        target_name: lista com o nome EXATO dos arquivos que devem ser substituídos. deve ser exato porque se não, nomes como "obs" e "obsidian"  
        seriam ambíguos por ambos terem "obs" presente no nome. deve incluir extensão, como .svg
          
        substitute_file: o path completo do arquivo pelo qual o alvo será substituídos
          
        destinations_dirs: lista de paths de diretórios onde a busca será feita.  
        todos os arquivos dentro desse diretório que baterem com o nome do target vão ser substituídos  
        é uma lista pra que diferentes versões do mesmo icon pack possam ser mudadas em uma chamada. ex: kora-light, kora-dark  
          
        force_creation_in: um valor opcional que define se a função vai ou não forçar a criação de arquivos que não existem  
        o diretório deve ser EXATO, não recursivo. se o valor estiver presente, já conta como confirmação de que deve ser feito
    """

    if not substitute_file.is_file():
        logger.error(f"o arquivo substituto {substitute_file} é inválido")
        return
    
    if force_creation_in is not None:
        logger.info(f"iniciando substituição. force_creation_in: True")
    else:
        logger.info(f"iniciando substituição. force_creation_in: False")

    for destination in destinations_dirs:
        if not destination.exists() or not destination.is_dir():
            logger.error(f"o diretório alvo {destination} não existe ou é inválido")
            continue

        # substituir os arquivos que têm o nome de cada target com o substituto
        for trg_name in target_names:
            # adicionar .svg no final do nome do alvo caso já não tenha
            if not trg_name.endswith(".svg"):
                trg_name += ".svg"
            
            # flag necessária em caso de force_creation
            found_existing_file = False

            for f in destination.rglob("*"): # rglob ao invés de iterdir pra que a busca seja recursiva
                if f.name == trg_name:
                    found_existing_file = True

                    try:
                        copy2(substitute_file, f)
                        logger.success(f"arquivo substituído: {f}")
                    except Exception as err:
                        logger.error(f"erro ao substituir {f}: {err}")
            
            # se não encontrou e o force_creation_in estiver setado e o destino atual for esse path
            if not found_existing_file and force_creation_in is not None and destination == force_creation_in.parent:
                new_file = force_creation_in / trg_name
                try:
                    # garante que o diretório existe
                    force_creation_in.mkdir(parents=True, exist_ok=True)
                    copy2(substitute_file, new_file)
                    logger.success(f"arquivo criado: {new_file}")
                except Exception as err:
                    logger.error(f"erro ao criar {new_file}: {err}")