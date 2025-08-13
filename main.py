import argparse
from pathlib import Path

from src import fetch, replace, switch, create, remove
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED, SUBSTITUTES_APPS, SUBSTITUTES_SYSTEM, SUBSTITUTES_PLACES, COPYCAT_REPO_MAIN
from maps import replace as replace_maps
from maps import fetch as fetch_maps
from maps import remove as remove_maps

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
        terms = fetch_maps.terms
        fetch.fetch(search_terms=terms, input_dir=ORIGINAL_UNZIPPED, output_dir=FETCH_OUTPUT)
    elif args.mode == "fetch" and args.clear:
        # rodar o clear caso o arg clear esteja presente
        fetch.clear(output_dir=FETCH_OUTPUT)
    
    if args.mode == "replace":
        if args.section == "software":
            replace_map = replace_maps.software
        elif args.section == "system":
            replace_map = replace_maps.system
        elif args.section == "places":
            replace_map = replace_maps.places
        else:
            # mudar tudo caso uma seção não seja especificada
            # | cria um novo dicionário juntando todos os outros
            replace_map = replace_maps.software | replace_maps.system | replace_maps.places

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
            # obter as flags, se presentes
            # o force_creation_in serve pra criação de ícones que podem não existir no pack original
            # assim, ao invés de só tentar substituir, se o ícone não existir, ele será criado caso seja true
            # o caminho onde essa criação deve acontecer acontece no dicionário de entradas
            # esse path deve ser a partir da raiz do icon pack. ex: kora, kora/apps/scalables
            #
            # e o ignore_key serve pra não procurar por ícones com o nome da chave em si, e sim só seus aliases
            # ele não é passado pra função diretamente porque nesse mesmo for, a chave só é
            # atribuída ao array de aliases se ele for true, então não precisa passar pra função explicitamente
            get_force_creation = entry.get("force_creation_in", None)
            ignore_key = entry.get("ignore_key", False)

            # adicionar key na lista de aliases (caso o campo de aliases exista e caso o ignore_key seja false)
            # por que em alguns casos um alias do software pode também ser a key
            aliases = entry.get("aliases", [])
            if not ignore_key: aliases.append(key)

            for dest in destinations:
                # montar o path de criação caso 
                if get_force_creation is not None:
                    # juntar o destino (que a raiz do icon pack) com o diretório do force
                    # que pode ser algo como apps/scalable
                    force_path = dest / get_force_creation

                    for alias in aliases:
                        # e depois adicionar o nome do arquivo novo no final
                        new_icon_name = alias + ".svg"

                        create.create(
                            target_path=force_path / new_icon_name,
                            file_to_create=entry["substitute"]
                        )

                # dest está entre colchetes pq a função original esperava uma lista
                # agora que a iteração é feita diretamente aqui pra poder ter precisão no force_path,
                # ela é feita assim, obtendo o índice atual da iteração de destinations
                replace.replace(
                    target_names=aliases,
                    substitute_file=entry["substitute"],
                    destinations_dirs=[dest],
                    #force_creation_in=force_path
                )

    if args.mode == "switch":
        copycat = Path("/home/luan/.local/share/icons/copycat")
        fluent = Path("/mnt/seagate/authoral-software/copykit/data/original-unzipped/Fluent-dark")

        # mais lugares onde os ícones do fluent podem estar espalhados
        fluent_variants = [
            fluent / "16",
            fluent / "24",
            fluent / "32",
            fluent / "256",
            fluent / "symbolic",
            #fluent / "22" # rodado por último pq esses ícones tem prioridade
        ]

        # nome de todos os diretórios do kora que tem um subdir chamado "symbolic" ou com uma variação numérica
        targets = ["apps", "actions", "status", "categories", "places", "devices", "emblems", "mimetypes"]

        for trg in targets:
            for fluent_var in fluent_variants:
                # ir nos diretórios symbolic de cada target
                switch.switch(
                    copycat / trg / "symbolic",
                    fluent_var / trg
                )

                # ir nos diretórios de ícones de tamanhos diferentes
                for numerical_variant in ["16", "22", "24", "32", "256"]:
                    switch.switch(
                        copycat / trg / numerical_variant,
                        fluent_var / trg
                    )

    # sempre rodar o remove independente do comando
    for icon_path in remove_maps.remove:
        icon_path = COPYCAT_REPO_MAIN / icon_path
        remove.remove(icon_path)

main()