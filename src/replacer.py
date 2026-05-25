from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import json
import shutil

from .globals import PACK_LOCAL, PACK_REMOTE, SUBSTITUTES, INSTRUCTIONS, normalize_json_name, normalize_svg_name
from . import logger


ACTIVE_ROOT = PACK_LOCAL
# ACTIVE_ROOT = PACK_REMOTE


@dataclass
class Context:
    """
    define o contexto base para resolução de caminhos e identificação do mapping

    args:
    	id:
    		identificador usado principalmente para logs e rastreamento

    	target_parent:
    		diretório base onde os targets estão localizados

    	substitute_parent:
    		diretório base onde os substitutos estão localizados, pode ser nulo
    """

    id: str # pra identificação nos logs
    data: dict
    # raw_target_parent: Path
    # raw_substitute_parent: Optional[Path] # pode ser nulo se não precisar

    @property
    def raw_context(self) -> dict:
        return self.data['context']

    @classmethod
    def from_dict(cls, data: dict, file: Path) -> Context:
        """
        resolve e valida o contexto a partir dos dados carregados de um json

        args:
            data:
                dicionário com os dados do json

            file:
                caminho do arquivo json, usado para mensagens de erro
        """
        
        raw_context = data['context']

        if not raw_context:
            raise ValueError(f'contexto não definido ({file.name})')

        id = raw_context.get('id')
        if not id:
            raise ValueError(f'id não definido ({file.name})')
        
        return cls(
            id=id,
            data=data
        )
    
    @property
    def target_parent(self) -> Path | None:
        # obter o parent do target e resolver o path
        raw = self.raw_context.get('target-parent')

        if not raw:
            return None

        if 'ROOT' not in raw:
            raise ValueError(f"'ROOT' precisa estar presente em target-parent ({id})")
        
        return Path(raw.replace('ROOT', str(ACTIVE_ROOT)))

    @property
    def substitute_parent(self) -> Path | None:
        # obter o parent do substituto e resolver o path
        raw = self.raw_context.get('substitute-parent')
        
        if not raw:
            return None
        
        if 'SUBSTITUTES' not in raw:
            raise ValueError(f"'SUBSTITUTES' precisa estar presente em substitute-parent ou ser completamente nulo ({id})")
        
        return Path(raw.replace('SUBSTITUTES', str(SUBSTITUTES)))


@dataclass
class Target:
    """
    representa um arquivo de destino que sofrerá alguma ação (create, replace, symlink ou remove)

    args:
    	icon:
    		nome lógico do ícone, usado para identificação e construção do caminho

    	action:
    		ação que será aplicada ao target (create, replace, symlink, remove)
            se for remove, não precisa ter substitute

    	path:
    		caminho absoluto do arquivo no sistema
    """
    
    icon: str # equivalente à name, TODO: talvez mudar pra name
    action: str
    path: Path

    def is_valid(self) -> bool:
        return self.path.exists() and self.path.is_file()


@dataclass
class Substitute:
    """
    representa um arquivo substituto que será usado em operações de create ou replace

    args:
    	name:
    		nome lógico do substituto, vindo do json

    	path:
    		caminho absoluto do arquivo substituto
    """

    name: str
    path: Path

    def is_valid(self) -> bool:
        return self.path.exists() and self.path.is_file()


@dataclass
class Entry:
    """
    agrupa um substituto opcional com uma lista de targets que compartilham esse substituto

    args:
    	substitute:
    		substituto associado aos targets,
            pode ser nulo para ações que não precisam dele, tipo remoções

    	targets:
    		lista de targets que serão processados
        
        symlink_to:
            pra onde o symlink deve apontar. só é necessário se a action do target for 'symlink' 

        changelog:
            mudanças que foram feitas no ícone

        sources:
            fontes de onde elementos do ícone vieram

        key:
            chave que identifica essa entry dentro do json de instruções, tipo "Discord"
            não tem função prática na substituição, mas é útil pra documentação
            é literalmente a chave de um dict, não é um valor definido dentro dele
    """

    key: str
    substitute: Optional[Substitute] # pode ser nulo se não precisar
    targets: List[Target]
    symlink_to: Optional[str]
    changelog: Optional[str]
    sources: Optional[list]

    @classmethod
    def from_dict(cls, data: dict, key: str, context: Context) -> Entry | None:
        # resolver o substitute
        substitute_name = data.get('substitute')
        substitute = None
        
        if substitute_name:
            if not context.substitute_parent:
                logger.warning(f'substitute definido, mas substitute-parent é inválido ({context.id})')
                return

            substitute = Substitute(
                name=substitute_name,
                path=context.substitute_parent / normalize_svg_name(substitute_name)
            )
        
        # resolver os targets e adicionar eles numa lista
        targets = []
        for raw_target in data.get('targets', []):
            icon = raw_target.get('icon')
            action = raw_target.get('action')

            if not icon or not action:
                logger.error(f'target inválido em {context.id}')
                continue
            
            path = context.target_parent / normalize_svg_name(icon)
            targets.append(Target(
                icon=icon,
                action=action,
                path=path
            ))

        return cls(
            key=key,
            substitute=substitute,
            targets=targets,
            symlink_to=data.get('symlink-to'), # TODO: mudar pra link_target ou canonical ou master
            changelog=data.get('changelog'),
            sources=data.get('sources')
        )


@dataclass
class Mapping:
    """
    representa uma unidade completa de instrução carregada de um json, contendo contexto e entries
    é equivalente ao .json pai das instruções

    args:
    	context:
    		contexto com informações base para resolução de caminhos

    	entries:
    		dicionário de entries indexadas por chave arbitrária do json
    """

    context: Context
    entries: dict[str, Entry] # TODO: talvez key na Entry não seja necessário pela key já estar presente aqui

    @classmethod
    def from_file(cls, file: Path) -> Mapping | None:
        """
        converte um arquivo json em um objeto mapping estruturado

        args:
            file:
                caminho do arquivo json contendo instruções
        """

        if not file.is_file():
            return
        
        with file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            logger.error(f'os dados obtidos de {file.name} são inválidos')
            return
        
        # transformar os dados do contexto num objeto
        try:
            context = Context.from_dict(data=data, file=file)
        except ValueError as err:
            logger.error(err)
            return

        # transformar as entries em um objeto
        entries = {}
        for key, raw_entry in data.get('entries', {}).items():
            e = Entry.from_dict(
                key=key,
                data=raw_entry,
                context=context
            )
            entries[key] = e

        mapping = Mapping(
            context=context,
            entries=entries
        )
        return mapping


def handle_create_or_replace(entry: Entry, target: Target, hard_replace: bool, skip_symlinks: bool):
    """
    lida com ações de criação ou substituição de arquivos a partir de um substituto

    args:
    	entry:
    		entry que contém o substituto e os targets associados

    	target:
    		target atual que define o caminho e a ação a ser executada

    	hard_replace:
    		define se a substituição deve ignorar validações do destino

    	skip_symlinks:
    		define se symlinks devem ser ignorados durante replace
    """
    
    # garantir que existe um substituto válido antes de qualquer operação
    substitute = entry.substitute

    if not substitute:
        logger.error(f'substituto não encontrado para {target.icon}')
        return
    
    if not substitute.is_valid():
        logger.error(f'substituto inválido: {substitute.path}')
        return
    
    # após ter um caminho de ícone substituto válido, as ações podem começar
    if target.action == 'replace':
        if not hard_replace:
            if not target.is_valid():
                logger.error(f'destino inválido: {target.path}')
                return
            
            if target.path.is_symlink() and skip_symlinks:
                logger.skip(f'symlink pulado: {target.icon}')
                return
    
        copy(substitute=substitute.path, destination=target.path, operation='substituído')
    elif target.action == 'create':
        copy(substitute=substitute.path, destination=target.path, operation='criado')

def handle_symlink(symlink_to: Path, target: Target):
    """
    cria um symlink apontando para o arquivo master previamente definido

    args:
    	symlink_to:
    		caminho do arquivo que será referenciado pelo symlink

    	target:
    		target que define onde o symlink será criado
    """
    
    # symlink depende de um arquivo base previamente definido
    if not symlink_to:
        logger.error(f'erro ao criar o symlink. um symlink-to ainda não foi definido para {target.icon}')
        return
    
    # deletar o antigo arquivo/symlink que possivelmente existe no destino do symlink novo
    link = target.path
    if link.exists() or link.is_symlink():
        link.unlink()

    # criar o symlink
    symlink_to = normalize_svg_name(symlink_to)
    link.symlink_to(symlink_to)

    if not link.exists() or not link.is_file():
        logger.error(f'{link} não foi criado como um symlink válido')
        return

    logger.symlink(f'symlink {link} criado para {target.path}')

def handle_remove(target: Target):
    """
    remove o arquivo ou symlink do target, se existir

    args:
    	target:
    		target que define o caminho do arquivo a ser removido
    """

    try:
        target.path.unlink()
        logger.success(f'{target.icon} deletado')
    except FileNotFoundError:
        logger.skip(f'{target.icon} não precisa ser deletado porque já não existe')
    except Exception as err:
        logger.error(f'erro ao deletar {target.icon}')
        logger.error(err)

# TODO: param (flag) pra chamar ou não o processor e otimizar os svgs ao copiar eles
def copy(substitute: Path, destination: Path, operation: str, ensure_parents: bool = True):
    """
    copia um arquivo substituto para o destino, removendo qualquer arquivo existente antes

    args:
    	substitute:
    		caminho do arquivo que será copiado

    	destination:
    		caminho onde o arquivo será colocado. isso já inclui o nome do arquivo
            não é só o parent de onde ele deve estar

    	operation:
    	    descrição textual da operação para logging. ex: 'criado', 'substituído'

        ensure_parents:
            garantir que a estrutura de diretórios pai exista, e criar caso não
    """

    try:
        # limpar o destino, removendo o alvo antes de substituir ele
        if destination.exists() or destination.is_symlink():
            try:
                destination.unlink()
            except Exception as err:
                logger.error(f'erro ao deletar {destination} para substituí-lo com {substitute}')
                logger.error(err)
        
        # criar a estrutura de dirs caso solicitado
        if ensure_parents:
            destination.parent.mkdir(exist_ok=True, parents=True)
            logger.success(f'estrutura de diretórios criada para {destination}')

        shutil.copy2(substitute, destination)
        logger.success(f'arquivo {operation}: {destination}')
    except Exception as err:
        logger.error(f'erro ao copiar o substituto {substitute} para {destination}')
        logger.error(err)

def replace(
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
        targets = entry.targets
        if not targets:
            logger.error(f'nenhum target encontrado para substituir em {id}')
            continue

        # reconstruir o caminho do ícone e fazer as mudanças
        for t in targets:
            action = t.action
            icon = t.icon

            if not icon:
                logger.error(f'target sem ícone em {id}')
                continue

            if not action:
                logger.error(f'ação não definida para {icon}')
                continue

            if action in ('create', 'replace'):
                # o caminho do ícone substituto só precisa ser reconstruído quando a action exigir ele
                # por isso esse if action in() é necessário, pra que outras acções que não precisem dele
                # não façam toda entrada dos json obrigatoriamente ter um campo substitute
                handle_create_or_replace(entry, t, hard_replace, skip_symlinks)
            elif action == 'symlink':
                symlink_to = entry.symlink_to

                if symlink_to:
                    logger.info(f'symlink-to definido como {symlink_to}')
                    handle_symlink(symlink_to, t)
                else:
                    logger.info(f'symlink-to não definido para {id}')
            elif action == 'remove':
                handle_remove(t)

def run(root: Path = PACK_LOCAL):
    """
    percorre todos os arquivos de instrução e executa o processo de replace para cada mapping

    args:
    	root:
    		caminho base do icon pack. ex: icons/copycat, icons/papirus
    """

    for f in INSTRUCTIONS.iterdir():
        mapping = Mapping.from_file(f)
        if not mapping:
            continue

        replace(mapping)

run(PACK_LOCAL)
# run(PACK_REMOTE)

# TODO: arrumar o PACK_LOCAL hardcoded em partes do código
# TODO: opção pra remover todos os symlinks quebrados depois de uma remoção