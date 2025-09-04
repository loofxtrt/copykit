import argparse
from pathlib import Path

from src import fetch, replace, create, remove, make_symlinks
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED, SUBSTITUTES_APPS, SUBSTITUTES_SYSTEM, SUBSTITUTES_PLACES, COPYCAT_REPO_MAIN
from src.utils import logger
from maps import replace as replace_maps
from maps import fetch as fetch_maps
from maps import remove as remove_maps

def set_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="fetch/replace/remove")
    parser.add_argument("--section", "-s", help="software/system/mimetypes, seção à qual o replace deve ser aplicado")
    parser.add_argument("--replacelevel", "-rl", help="repo/local, se presente, define se só o repo ou o local vai ser atualizado. se não, atualiza os dois")
    parser.add_argument("--clear", "-c", action="store_true", help="limpa o diretório de output")
    parser.add_argument("--limited", "-l", help="nome de uma chave do replace específica pra ser substituída, ignorando outros arquivos")

    return parser

def normalize_svg_name(name: str):
    if not name.endswith(".svg"):
        return name + ".svg"
    else:
        return name

def wrap_make_symlinks(pack_root: Path, symlinks_dir: Path, new_main_icon_name: str, aliases: list[str], substitute_file: Path):
    # montar o diretório onde os symlinks vão ser criados
    target_dir = pack_root / symlinks_dir

    if not target_dir.exists():
        logger.error(f"caminho inválido: {target_dir}"); return

    # deletar todos os svgs com nomes que batem com os aliases
    if aliases:
        for alias in aliases:
            alias = normalize_svg_name(alias)
            
            full_path = target_dir / alias
            if full_path.exists() or full_path.is_symlink():
                Path.unlink(full_path);
                logger.info(f"ícone deletado: {alias}")
            
    # criar o ícone principal
    svg_name = normalize_svg_name(new_main_icon_name)

    main_icon = target_dir / svg_name
    create.create(
        target_path=target_dir / main_icon,
        file_to_create=substitute_file
    )

    # criar os symlinks apontando pro ícone principal
    for alias in aliases:
        alias = normalize_svg_name(alias)

        make_symlinks.make_symlinks(
            original_file=main_icon,
            new_symlink=target_dir / alias
        )

def wrap_force_creation(pack_root: Path, aliases: list[str]):
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

def handle_replace(args, destinations: list[Path]):
    """
        force_creation_in serve pra criação de ícones que podem não existir no pack original
        assim, ao invés de só tentar substituir, se o ícone não existir, ele será criado caso seja true
        o caminho onde essa criação deve acontecer acontece no dicionário de entradas
        esse path deve ser a partir da raiz do icon pack. ex: kora, kora/apps/scalables
    
        ignore_key serve pra não procurar por ícones com o nome da chave em si, e sim só seus aliases
        ele não é passado pra função diretamente porque nesse mesmo for, a chave só é
        atribuída ao array de aliases se ele for true, então não precisa passar pra função explicitamente

        delete_aliases_make_symlinks_at serve pra deletar todos as instâncias daquele ícone
        antes de criar o ícone principal (o primeiro do array de aliases)
        e depois fazer todos os aliases virarem symlinks pro principal
        isso é útil em casos de repetição extrema, como mimetypes zippados, pra substituir por um único ícone de zip
        os valores atribuidos a essa chave devem ser [bool, path pra onde deve ser criado o principal e os symlinks]
    """

    # definir quais seções vão ser obedecidas. se uma não for especificada, vão ser todas
    # software, system, places mimetypes etc.
    if args.section:
        rep_map = replace_maps.args.section

        if not rep_map:
            logger.error("seção inválida")
            return
    else:
        rep_map = replace_maps.software | replace_maps.system | replace_maps.places | replace_maps.mimetypes
    
    for key, entry in rep_map.items():
        # se a opção limited estiver ativo e a chave não for a da opção, pula
        if args.limited and not key == args.limited:
            logger.info(f"pulando chave {key} pelo modo limitado"); continue
        
        logger.info(f"requisição de substituição iniciado na chave {key}")

        # obter as flags, se alguma delas estiver presentes na entrada do replace_map
        ignore_key = entry.get("ignore_key", False)
        make_symlinks_at = entry.get("delete_aliases_make_symlinks_at", None)

        # adicionar key na lista de aliases (caso o campo de aliases exista e caso o ignore_key seja false)
        # em alguns casos a key é só um nome representativo, enquanto os nomes reais estão nos aliases
        aliases = entry.get("aliases", [])
        if not ignore_key: aliases.append(key)

        for dest in destinations:
            # criar os symlinks e parar a substituição, pq a criação deles já conta como uma
            if make_symlinks_at is not None:
                main_icon_name = key if not ignore_key else aliases[0]

                wrap_make_symlinks(dest, make_symlinks_at, main_icon_name, aliases, entry["substitute"])
                continue
            
            replace.replace(
                target_names=aliases,
                substitute_file=entry["substitute"],
                destinations_dirs=[dest]
            )


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
        
        handle_replace(args, destinations)

    # sempre rodar o remove independente do comando
    #for icon_path in remove_maps.remove:
    #    icon_path = COPYCAT_REPO_MAIN / icon_path
    #    remove.remove(icon_path)

main()