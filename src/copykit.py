from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import json
import shutil
import argparse

from rich.console import Console
from rich.text import Text

from .utils import normalize_json_name, normalize_svg_name, read_json, write_json, drop_empty, read_toml
from .models import Entry, Target, Mapping, Context, Substitute, Environment
from .handlers import remove, replace, symlink
from .logger import EntryLogger
from .documenter import run_documenter
from . import logger, processor


# TODO: template de index.theme


class CLI:
    # TODO: documentação
    
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            '--environment',
            '-e',
            type=Path,
            required=True,
            help='arquivo toml que representa um environment'
        )

        self.subparsers = self.parser.add_subparsers(
            dest='command',
            required=True
        )

        self._register_apply()
        self._register_docs()

    def execute(self):
        args = self.parser.parse_args()
    
        environment = args.environment
        if not environment.is_file():
            logger.error('o environment deve ser um toml')
            return
        self.environment = Environment.from_dict(read_toml(environment))

        args.func(args)

    def _register_apply(self):
        parser_apply = self.subparsers.add_parser('apply')
        parser_apply.add_argument(
            '--level',
            '-l',
            choices=['local', 'stable'],
            default='local'
        )
        parser_apply.set_defaults(func=self.cmd_apply)
    
    def _register_docs(self):
        parser_docs = self.subparsers.add_parser('docs')
        parser_docs.set_defaults(func=self.cmd_docs)

    def cmd_apply(self, args):
        if args.level == 'local':
            run_copykit(self.environment, self.environment.pack_local)
        elif args.level == 'stable':
            run_copykit(self.environment, self.environment.pack_stable)
    
    def cmd_docs(self, args):
        run_documenter(environment=self.environment)


def handle_mapping(
    mapping: Mapping,
    skip_symlinks: bool = True,
    hard_replace: bool = True
    ):
    """
    executa todas as ações definidas em um mapping, como create, replace, symlink e remove

    args:
    	mapping:
    		objeto contendo contexto e entries com instruções de manipulação de arquivos

    	skip_symlinks:
    		define se symlinks existentes devem ser ignorados durante replace

    	hard_replace:
    		define se replace deve ocorrer mesmo sem validação do destino
    """

    # validação informações básicas do mapping
    context = mapping.context
    target_parent = context.target_parent
    substitute_parent = context.substitute_parent
    _id = context.id

    if not target_parent.is_dir():
        logger.error(f'{target_parent} não é um diretório')
        return
    
    if substitute_parent is not None:
        if not substitute_parent.is_dir():
            logger.error(f'{substitute_parent} está presente, mas não é um diretório')
            return

    # começar as operações
    entries = mapping.entries
    if not entries:
        logger.error(f'nenhuma entry presente em {_id}')
        return
    
    for entry in mapping.entries.values():
        # criar o logger dessa entry específica
        entry_logger = EntryLogger(
            title=entry.key,
            prefix=f'{_id}:'
        )
        
        targets = entry.targets
        if not targets:
            entry_logger.error(f'nenhum target encontrado para substituir em {_id}')
            continue
        
        canonical = entry.canonical
        if canonical:
            entry_logger.info(f'canonical definido como {canonical}')

        # reconstruir o caminho do ícone e fazer as mudanças
        for t in targets:
            action = t.action
            icon = t.icon

            if not icon:
                entry_logger.error(f'target sem ícone em {_id}')
                continue

            if not action:
                entry_logger.error(f'ação não definida para {icon}')
                continue

            if action in ('create', 'replace'):
                # TODO: comentário desatualizado
                # o caminho do ícone substituto só precisa ser reconstruído quando a action exigir ele
                # por isso esse if action in() é necessário, pra que outras acções que não precisem dele
                # não façam toda entrada dos json obrigatoriamente ter um campo substitute
                replace.handle_create_or_replace(
                    entry=entry,
                    target=t,
                    context=context,
                    hard_replace=hard_replace,
                    skip_symlinks=skip_symlinks,
                    logger=entry_logger
                )
            elif action == 'symlink':
                if not canonical:
                    entry_logger.info(f'canonical não definido para {_id}')
                    continue

                symlink.handle_symlink(
                    canonical=canonical,
                    target=t,
                    logger=entry_logger,
                    context=context
                )
            elif action == 'remove':
                remove.handle_remove(
                    target=t,
                    context=context,
                    logger=entry_logger
                )
        
        # IMPORTANTE
        # fechar o ambiente vivo desse logger quando terminar o processamento
        entry_logger.close()

def run_copykit(environment: Environment, active_root: Path):
    """
    percorre todos os arquivos de instrução e executa o processo de replace para cada mapping

    args:
    	environment:
    		ambiente, o icon pack esse contexto trabalha sobre

        active_root:
            icon pack a ser afetado
    """

    for f in environment.mappings.iterdir():
        m = Mapping.from_file(file=f, active_root=active_root, environment=environment)
        if not m:
            continue

        handle_mapping(m)

    # TODO: fazer panel costum pro rich e desaclopar do logger de entry    
    # console = Console()
    # text = Text()
    # text.append('')

def main():
    CLI().execute()

if __name__ == '__main__':
    main()

# TODO: opção pra remover todos os symlinks quebrados depois de uma remoção
# TODO: aviso de se um mapping não tem um substitute parent definido
# TODO: remover código morto
# TODO: melhorar segurança em relação a root opcional
# TODO: erro quando uma action não existe
# TODO: dataclass pra sources?
# TODO: aplicar processing de optimize por padrão ou criar um bash que aplique
# TODO: contexto pai declarativo, tipo substitutes, root etc. todos definidos num arquivo em vez de no código