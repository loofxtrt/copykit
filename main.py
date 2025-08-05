import argparse
from pathlib import Path

from src import fetch, replace, switch
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED, SUBSTITUTES_APPS, SUBSTITUTES_SYSTEM, SUBSTITUTES_PLACES
import maps

def set_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="fetch/replace/switch")
    parser.add_argument("--section", "-s", help="software/system, seção à qual o replace deve ser aplicado")
    parser.add_argument("--replacelevel", "-rl", help="repo/local, se presente, define se só o repo ou o local vai ser atualizado. se não, atualiza os dois")
    parser.add_argument("--clear", "-c", action="store_true", help="limpa o diretório de output")

    return parser

def main():
    parser = set_parser()
    args = parser.parse_args()

    if args.mode == "fetch" and not args.clear:
        # obter os termos de pesquisa e rodar o fetch
        terms = maps.fetch.terms
        fetch.fetch(search_terms=terms, input_dir=ORIGINAL_UNZIPPED, output_dir=FETCH_OUTPUT)
    elif args.mode == "fetch" and args.clear:
        # rodar o clear caso o arg clear esteja presente
        fetch.clear(output_dir=FETCH_OUTPUT)
    
    if args.mode == "replace":
        if args.section == "software":
            replace_map = maps.replace.software
        elif args.section == "system":
            replace_map = maps.replace.system
        elif args.section == "places":
            replace_map = maps.replace.places
        else:
            # mudar tudo caso uma seção não seja especificada
            replace_map = maps.replace.software + maps.replace.system + maps.replace.places

        repo_destinations = [
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat"),
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat-light"),
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat-light-panel")
        ]

        local_destinations = [
            Path("/home/luan/.local/share/icons/copycat"),
            #Path("/home/luan/.local/share/icons/copycat-light"),
            #Path("/home/luan/.local/share/icons/copycat-light-panel")
        ]

        if args.replacelevel == "repo":
            # atualizar o repo dos ícones
            destinations = repo_destinations
        elif args.replacelevel == "local":
            # atualizar só localmente
            destinations = local_destinations
        else:
            # atualizar os dois
            destinations = repo_destinations + local_destinations

        # obter os valores do replace_map, obttendo a chave e os valores das entradas
        # então, pra cada 
        for key, entry in replace_map.items():
            # adicionar key na lista de aliases (caso o campo de aliases exista)
            # por que em alguns casos um alias do software pode também ser a key
            aliases = entry.get("aliases", [])
            aliases.append(key)

            replace.replace(
                target_names=aliases,
                substitute_file=entry["substitute"],
                destinations_dirs=destinations
            )

    if args.mode == "switch":
        switch.switch(
            #target_dir=Path("/mnt/seagate/symlinks/kde-user-icons/copycat/apps/symbolic/"),
            #source_dir=Path("/mnt/seagate/symlinks/copykit-data/data/original-unzipped/Fluent-dark/symbolic/apps/")

            #target_dir=Path("/mnt/seagate/symlinks/kde-user-icons/copycat/actions/symbolic/"),
            #source_dir=Path("/mnt/seagate/symlinks/copykit-data/data/original-unzipped/Fluent-dark/symbolic/actions/")
        
            target_dir=Path("/mnt/seagate/symlinks/kde-user-icons/copycat/status/symbolic/"),
            source_dir=Path("/mnt/seagate/symlinks/copykit-data/data/original-unzipped/Fluent-dark/symbolic/status/")
        )

main()