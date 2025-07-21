from pathlib import Path
from shutil import copy2, rmtree

from src.utils import logger

def clear(output_dir: Path):
    """
        limpa o diretório de output especificado
    """

    # iterar cada arquivo do diretório passado pra função e deletar ele caso seja um arquivo ou diretório
    for item in output_dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            rmtree(item)

def fetch(search_term: str, input_dir: Path, output_dir: Path):
    """
        encontra todos os arquivos que contém o search_term em seu nome dentro do input_dir  
        e então, copia esses arquivos pro output_dir, identificando o pack de ícones de onde cada um vem  
        adicionando o nome desse pack (o diretório pai relativo ao input) no ínicio do nome do arquivo copiado
    """

    # criar o diretório de output caso ele não exista
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # pesquisar nesse diretório todos os arquivos que tenham o search_term no nome
    for f in input_dir.rglob("*"):
        if f.is_file() and search_term in f.name.lower():
            try:
                # obter o nome do diretório pai de onde o ícone vem, relativo ao input_dir
                # ex: "mnt/projects/icons/unzipped/icones/flor.png" = Path("icones/flor.png")
                # e depois usar parts no Path pra transformar em uma tupla de pedaços. ex: ('icones', 'flor.png')
                # e parts[0] obtem 'icones' que é o índice 0
                parent_pack = f.relative_to(input_dir).parts[0]
                parent_pack = parent_pack.lower()
            except Exception:
                # previnir caso um arquivo não esteja em uma subpasta, o que poderia quebrar o parts
                # ex, não daria pra usar parts[0] em "unzipped/flor_sem_pasta.png" pq não é uma tupla
                logger.error("o arquivo encontrado não possui um diretório pai")
                continue
            
            # montar o novo path e copiar o arquivo pro destino final
            new_path = output_dir / f"{parent_pack}_{f.name}"
            copy2(f, new_path)

            logger.info(f"arquivo encontrado em {parent_pack}: {f.name}")