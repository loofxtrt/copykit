from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import json
import shutil
import argparse

from pathvalidate import sanitize_filename
from prompt_toolkit import PromptSession

from .globals import PACK_LOCAL, PACK_REMOTE, SUBSTITUTES, INSTRUCTIONS, normalize_json_name, normalize_svg_name, read_json, write_json
from .models import Entry, Target, Mapping, Context, Substitute
from .handlers import remove, replace, symlink
from .logger import EntryLogger
from .documenter import run_documenter
from . import logger, processor


class CLI:
    # TODO: documentação
    
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.subparsers = self.parser.add_subparsers(
            dest='command',
            required=True
        )

        self._register_apply()
        self._register_docs()
        self._register_mkmap()
        self._register_entry()
        self._register_map()

    def execute(self):
        args = self.parser.parse_args()
        args.func(args)

    def _register_apply(self):
        parser_apply = self.subparsers.add_parser('apply')
        parser_apply.add_argument(
            '--root',
            '-r',
            choices=['local', 'remote'],
            default='local'
        )
        parser_apply.set_defaults(func=self.cmd_apply)
    
    def _register_docs(self):
        parser_docs = self.subparsers.add_parser('docs')
        parser_docs.set_defaults(func=self.cmd_docs)
    
    def _register_mkmap(self):
        parser_mkmap = self.subparsers.add_parser('mkmap')
        parser_mkmap.add_argument(
            '--id',
            '-i',
            required=True
        )
        parser_mkmap.set_defaults(func=self.cmd_mkmap)
    
    def _register_map(self):
        parser_map = self.subparsers.add_parser('map')
        parser_map.add_argument(
            '--mapping-file',
            '-mf',
            required=True
        )
        parser_map.set_defaults(func=self.cmd_map)

    def _register_entry(self):
        parser_entry = self.subparsers.add_parser('entry')
        parser_entry.add_argument(
            '--mode',
            '-m',
            choices=['new', 'entry', 'target', 'source'],
            required=True
        )
        parser_entry.add_argument(
            '--key',
            '-k',
            required=True
        )
        parser_entry.add_argument(
            '--mapping-file',
            '-mf',
            required=True,
            help="""caminho relativo do mapping a partir do diretório de instruções,
            ex: PATH_INSTRUCOES + -mf apps/apps-simbolicos.json -> PATH_INSTRUCOES/apps/apps-simbolicos.json"""
        )
        parser_entry.set_defaults(func=self.cmd_entry)

    def cmd_apply(self, args):
        if args.root == 'local':
            run_copykit(PACK_LOCAL)
        elif args.root == 'remote':
            # run_copykit(PACK_REMOTE)
            pass
    
    def cmd_docs(self, args):
        run_documenter()

    def cmd_mkmap(self, args):
        # sanitizar o id passado como arg e usar ele como nome do arquivo (só conveniência)
        filename = normalize_json_name(sanitize_filename(args.id))
        file = INSTRUCTIONS / filename
        
        if file.exists():
            # TODO: raise de fileexists
            logger.error(f'um json de mapping com o mesmo nome já existe: {file.name}')
            return
        
        context = {
            'id': args.id
        }
        
        # obter dados opcionais e adiciona-los no contexto caso existam
        target_parent = input('target_parent: ROOT/')
        substitute_parent = input('substitute_parent: SUBSTITUTES/')
        
        if target_parent:
            context['target_parent'] = 'ROOT/' + target_parent
        if substitute_parent:
            context['substitute_parent'] = 'SUBSTITUTES/' + substitute_parent

        mapping = {
            'context': context,
            'entries': {}
        }

        # escrever o json final
        write_json(file, mapping)

    def cmd_map(self, args):
        shell(INSTRUCTIONS / args.mapping_file)

    def cmd_entry(self, args):
        key = args.key
        
        # resolver qual mapping é o alvo da edição
        mapping_file = INSTRUCTIONS / args.mapping_file
        if not mapping_file.exists():
            logger.error(f'arquivo mapping não existe: {mapping_file}')

        mapping = Mapping.from_file(mapping_file)

        # delegar ações com base no modo do comando
        if args.mode == 'new':
            # obter outros campos opcionais
            substitute = input('substitute: ')
            canonical = input('canonical: ')
            changelog = input('changelog: ')

            data = {}

            if substitute:
                data['substitute'] = substitute
            if canonical:
                data['canonical'] = canonical
            if changelog:
                data['changelog'] = changelog
            
            # adicionar os dados obtidos no mapping
            # TODO: substitute exige path e isso quebra pq não dá pra serializar
            #       e faz ele nunca nem ser escrito no json
            new_entry = Entry.from_dict(data=data, key=key, context=mapping.context)
            mapping.insert_entry(key=key, entry=new_entry)
        elif args.mode == 'target':
            icon = input('icon: ')
            action = input('action: ')

            if not icon or not action:
                logger.error('impossível continuar sem um icon e action pro novo target')
                return

            target = Target(icon=icon, action=action)
            mapping.entries[key].insert_target(target)
        elif args.mode == 'source':
            source = input('source: ')
            used = input('used: ')
            single_asset = input('(single) asset: ') # single temporário pra não ter que tratar lista no cli
            
            assets = None
            if single_asset:
                assets = [single_asset]

            mapping.entries[key].insert_source(
                source=source,
                assets=assets,
                used=used
            )
        
        # salvar as mudanças no disco
        mapping.save_to_disk(mapping_file)


def shell(mapping_file: Path):
    def prompt(text: str | None = None):
        # refletir o estado atual do shell no prompt
        prefix = f'{mapping.context.id}'

        if key is not None:
            prefix += f' (entry:{key})'

        # mostrar > se for comando normal
        # ou : se for um prompt requerindo algo
        if text:
            prefix += f' {text}'
            prefix += ': '
        else:
            prefix += ' > '

        # promptar
        return session.prompt(prefix)

    def _save_mapping():
        mapping.save_to_disk(mapping_file)

    mapping = Mapping.from_file(mapping_file)
    key = None
    
    session = PromptSession()

    while True:
        try:
            cmd = prompt()

            if cmd == 'exit' or cmd == 'quit':
                break
            if cmd == 'entry':
                key = prompt('key')
                
                substitute = prompt('substitute')
                canonical = prompt('canonical')
                changelog = prompt('changelog')

                data = {}

                if substitute:
                    data['substitute'] = substitute
                if canonical:
                    data['canonical'] = canonical
                if changelog:
                    data['changelog'] = changelog
                
                # adicionar os dados obtidos no mapping
                new_entry = Entry.from_dict(data=data, key=key, context=mapping.context)
                
                mapping.insert_entry(key=key, entry=new_entry)
                _save_mapping()
            
            if key:
                if cmd == 'target':
                    icon = input('icon: ')
                    action = input('action: ')

                    if not icon or not action:
                        logger.error('impossível continuar sem um icon e action pro novo target')
                        return

                    target = Target(icon=icon, action=action)
                    mapping.entries[key].insert_target(target)

                    _save_mapping()
                elif cmd == 'source':
                    source = input('source: ')
                    used = input('used: ')
                    single_asset = input('(single) asset: ') # single temporário pra não ter que tratar lista no cli
                    
                    assets = None
                    if single_asset:
                        assets = [single_asset]

                    mapping.entries[key].insert_source(
                        source=source,
                        assets=assets,
                        used=used
                    )

                    _save_mapping()
                elif cmd == '..': # voltar ao mapping anterior depois de ter entrado numa entry
                    key = None
        except KeyboardInterrupt:
            # aceitar ctrl + c pra fechar
            break
    


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
    target_parent = mapping.context.target_parent
    substitute_parent = mapping.context.substitute_parent
    id = mapping.context.id

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
        logger.error(f'nenhuma entry presente em {id}')
        return
    
    for entry in mapping.entries.values():
        # criar o logger dessa entry específica
        entry_logger = EntryLogger(
            title=entry.key,
            prefix=f'{id}:'
        )
        
        targets = entry.targets
        if not targets:
            entry_logger.error(f'nenhum target encontrado para substituir em {id}')
            continue
        
        canonical = entry.canonical
        if canonical:
            entry_logger.info(f'canonical definido como {canonical}')

        # reconstruir o caminho do ícone e fazer as mudanças
        for t in targets:
            action = t.action
            icon = t.icon

            if not icon:
                entry_logger.error(f'target sem ícone em {id}')
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
                    hard_replace=hard_replace,
                    skip_symlinks=skip_symlinks,
                    logger=entry_logger
                )
            elif action == 'symlink':
                if not canonical:
                    entry_logger.info(f'canonical não definido para {id}')
                    continue

                symlink.handle_symlink(
                    canonical=canonical,
                    target=t,
                    logger=entry_logger
                )
            elif action == 'remove':
                remove.handle_remove(
                    target=t,
                    logger=entry_logger
                )
        
        # IMPORTANTE
        # fechar o ambiente vivo desse logger quando terminar o processamento
        entry_logger.close()

def run_copykit(root: Path):
    """
    percorre todos os arquivos de instrução e executa o processo de replace para cada mapping

    args:
    	root:
    		caminho base do icon pack. ex: icons/copycat, icons/papirus
    """

    for f in INSTRUCTIONS.iterdir():
        mapping = Mapping.from_file(file=f, active_root=root)
        if not mapping:
            continue

        handle_mapping(mapping)

def main():
    CLI().execute()

if __name__ == '__main__':
    main()

# TODO: opção pra remover todos os symlinks quebrados depois de uma remoção
# TODO: aviso de se um mapping não tem um substitute parent definido
# TODO: remover código morto
# TODO: melhorar segurança em relação a root opcional