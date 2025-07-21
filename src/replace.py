from pathlib import Path
from shutil import copy2

from src.utils import logger

def replace(target_names: list, substitute_file: Path, destinations_dirs: list[Path]):
    """
        target_name: lista com o nome EXATO dos arquivos que devem ser substituídos. deve ser exato porque se não, nomes como "obs" e "obsidian"  
        seriam ambíguos por ambos terem "obs" presente no nome. deve incluir extensão, como .svg
          
        substitute_file: o path completo do arquivo pelo qual o alvo será substituídos
          
        destinations_dirs: lista de paths de diretórios onde a busca será feita.  
        todos os arquivos dentro desse diretório que baterem com o nome do target vão ser substituídos  
        é uma lista pra que diferentes versões do mesmo icon pack possam ser mudadas em uma chamada. ex: kora-light, kora-dark
    """

    if not substitute_file.is_file():
        logger.error(f"o arquivo substituto {substitute_file} é inválido")
        return

    for destination in destinations_dirs:
        if not destination.exists() or not destination.is_dir():
            logger.error(f"o diretório alvo {destination} não existe ou é inválido")
            continue

        # substituir os arquivos que têm o nome de cada target com o substituto
        for tname in target_names:
            # adicionar .svg no final do nome do alvo caso já não tenha
            if not tname.endswith(".svg"):
                tname += ".svg"

            count = 0
            for f in destination.rglob("*"): # rglob ao invés de iterdir pra que a busca seja recursiva
                if f.name == tname:
                    try:
                        copy2(substitute_file, f)
                        logger.info(f"arquivo substituídos: {f}")
                        count += 1
                    except Exception as err:
                        logger.error(f"erro ao substituir {f}: {err}")

            if count == 0:
                logger.info(f"nenhum arquivo chamado {tname} foi encontrado em {destination}")
            else:
                logger.success(f"{count} arquivos substituídos")