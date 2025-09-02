import argparse
from pathlib import Path

from src import fetch, replace, switch, create, remove, make_symlinks
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED, SUBSTITUTES_APPS, SUBSTITUTES_SYSTEM, SUBSTITUTES_PLACES, COPYCAT_REPO_MAIN
from maps import replace as replace_maps
from maps import fetch as fetch_maps
from maps import remove as remove_maps

def set_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="fetch/replace/switch/remove")
    parser.add_argument("--section", "-s", help="software/system/mimetypes, seção à qual o replace deve ser aplicado")
    parser.add_argument("--replacelevel", "-rl", help="repo/local, se presente, define se só o repo ou o local vai ser atualizado. se não, atualiza os dois")
    parser.add_argument("--clear", "-c", action="store_true", help="limpa o diretório de output")
    parser.add_argument("--limited", "-l", help="nome de uma chave do replace específica pra ser substituída, ignorando outros arquivos")

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
        elif args.section == "mimetypes":
            replace_map = replace_maps.mimetypes
        else:
            # mudar tudo caso uma seção não seja especificada
            # | cria um novo dicionário juntando todos os outros
            replace_map = replace_maps.software | replace_maps.system | replace_maps.places | replace_maps.mimetypes

        repo_destinations = [
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat"),
            #Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat-light"),
            #Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat-light-panel")
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

        # obter os valores do replace_map, obtendo a chave e os valores das entradas
        for key, entry in replace_map.items():
            """
                force_creation_in serve pra criação de ícones que podem não existir no pack original
                assim, ao invés de só tentar substituir, se o ícone não existir, ele será criado caso seja true
                o caminho onde essa criação deve acontecer acontece no dicionário de entradas
                esse path deve ser a partir da raiz do icon pack. ex: kora, kora/apps/scalables
            
                ignore_key serve pra não procurar por ícones com o nome da chave em si, e sim só seus aliases
                ele não é passado pra função diretamente porque nesse mesmo for, a chave só é
                atribuída ao array de aliases se ele for true, então não precisa passar pra função explicitamente

                delete_aliases_make_symlinks serve pra deletar todos as instâncias daquele ícone
                antes de criar o ícone principal (o primeiro do array de aliases)
                e depois fazer todos os aliases virarem symlinks pro principal
                isso é útil em casos de repetição extrema, como mimetypes zippados, pra substituir por um único ícone de zip
                os valores atribuidos a essa chave devem ser [bool, path pra onde deve ser criado o principal e os symlinks]
            """

            if args.limited:
                if not key == args.limited:
                    print("ignorado: " + key)
                    continue

            print("iniciando substituição: " + key)

            # obter as flags, se presentes
            get_force_creation = entry.get("force_creation_in", None)
            ignore_key = entry.get("ignore_key", False)
            delete_aliases_make_symlinks = entry.get("delete_aliases_make_symlinks", [False, None])

            # adicionar key na lista de aliases (caso o campo de aliases exista e caso o ignore_key seja false)
            # porque em alguns casos a key é só um nome representativa, enquanto os nomes reais estão nos aliases
            aliases = entry.get("aliases", [])
            if not ignore_key: aliases.append(key)

            for dest in destinations:
                # montar o path de criação caso o force creation esteja presente
                if get_force_creation is not None:
                    # juntar o destino (que é a raiz do icon pack) com o diretório do force
                    # que pode ser algo como apps/scalable
                    force_path = dest / get_force_creation

                    # obter o ícone principal, o que vai ser usado de referência caso precise de symlinks
                    first_icon_name = aliases[0]

                    for alias in aliases:
                        # formatar o novo nome do arquivo
                        new_icon_name = alias + ".svg"

                        # criar uma cópia real APENAS se o índice for 0, o ícone principal
                        # caso contrário, criar só symlinks que apontem pra este
                        if alias == first_icon_name:
                            create.create(
                                target_path=force_path / new_icon_name,
                                file_to_create=entry["substitute"]
                            )
                        else:
                            create.create(
                                target_path=force_path / new_icon_name,
                                file_to_create=entry["substitute"],
                                as_symlink_to=force_path / (first_icon_name + ".svg")
                            )

                # deletar os aliases, criar um ícone principal, e recriar os aliases como symlinks
                # caso o delete_aliases_make_symlinks seja true
                if delete_aliases_make_symlinks[0]:
                    target_dir = dest / delete_aliases_make_symlinks[1]
                    print(target_dir)

                    if not ignore_key:
                        main_icon = target_dir / (key + ".svg")
                    else:
                        main_icon = target_dir / aliases[0] + ".svg"

                    # deletar
                    for alias in aliases:
                        if not alias.endswith(".svg"):
                            alias += ".svg"

                        full_alias_path = target_dir / alias
                        if full_alias_path.exists() or full_alias_path.is_symlink():
                            Path.unlink(full_alias_path)
                            print("deletado: " + str(full_alias_path))

                    # criar o ícone principal
                    create.create(
                        target_path=target_dir / key,
                        file_to_create=entry["substitute"]
                    )

                    # criar os symlinks
                    for alias in aliases:
                        if not alias.endswith(".svg"):
                            alias += ".svg"

                        make_symlinks.make_symlinks(
                            original_file=main_icon,
                            new_symlink=target_dir / alias
                        )

                    # não continuar a substituição, pq um equivalente dela já foi feita
                    continue

                # dest está entre colchetes pq a função original esperava uma lista
                # agora que a iteração é feita diretamente aqui pra poder ter precisão no force_path,
                # ela é feita assim, obtendo o índice atual da iteração de destinations
                replace.replace(
                    target_names=aliases,
                    substitute_file=entry["substitute"],
                    destinations_dirs=[dest],
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
    #for icon_path in remove_maps.remove:
    #    icon_path = COPYCAT_REPO_MAIN / icon_path
    #    remove.remove(icon_path)

main()