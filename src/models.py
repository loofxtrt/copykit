from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import json

from .globals import PACK_LOCAL, PACK_REMOTE, SUBSTITUTES, INSTRUCTIONS, normalize_json_name, normalize_svg_name
from . import logger


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

    # TODO: atualizar documentação

    id: str # pra identificação nos logs
    data: dict
    active_root: Path
    # raw_target_parent: Path
    # raw_substitute_parent: Optional[Path] # pode ser nulo se não precisar

    @property
    def raw_context(self) -> dict:
        return self.data['context']

    @classmethod
    def from_dict(cls, data: dict, file: Path, active_root: Path) -> Context:
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
            data=data,
            active_root=active_root
        )
    
    @property
    def target_parent(self) -> Path | None:
        # obter o parent do target e resolver o path
        raw = self.raw_context.get('target_parent')

        if not raw:
            return None

        if 'ROOT' not in raw:
            raise ValueError(f"'ROOT' precisa estar presente em target_parent ({id})")
        
        return Path(raw.replace('ROOT', str(self.active_root)))

    @property
    def substitute_parent(self) -> Path | None:
        # obter o parent do substituto e resolver o path
        raw = self.raw_context.get('substitute_parent')
        
        if not raw:
            return None
        
        if 'SUBSTITUTES' not in raw:
            raise ValueError(f"'SUBSTITUTES' precisa estar presente em substitute_parent ou ser completamente nulo ({id})")
        
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
        
        canonical:
            pra onde o symlink deve apontar. só é necessário se a action do target for 'symlink' 

        changelog:
            mudanças que foram feitas no ícone

        sources:
            fontes de onde elementos do ícone vieram

        key:
            chave que identifica essa entry dentro do json de instruções, tipo "Discord"
            não tem função prática na substituição, mas é útil pra documentação
            é literalmente a chave de um dict, não é um valor definido dentro dele
        
        processing:
            pós processamento que deve ser aplicado ao ícone
    """

    key: str
    substitute: Optional[Substitute] # pode ser nulo se não precisar
    targets: List[Target]
    canonical: Optional[str]
    changelog: Optional[str]
    sources: Optional[list]
    processing: Optional[str]

    @classmethod
    def from_dict(cls, data: dict, key: str, context: Context) -> Entry | None:
        # resolver o substitute
        substitute_name = data.get('substitute')
        substitute = None
        
        if substitute_name:
            if not context.substitute_parent:
                logger.warning(f'substitute definido, mas substitute_parent é inválido ({context.id})')
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
            canonical=data.get('canonical'),
            changelog=data.get('changelog'),
            sources=data.get('sources'),
            processing=data.get('processing')
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
    def from_file(cls, file: Path, active_root: Path) -> Mapping | None:
        """
        converte um arquivo json em um objeto mapping estruturado

        args:
            file:
                caminho do arquivo json contendo instruções
        """

        # TODO: atualizar documentação

        if not file.is_file():
            return
        
        with file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            logger.error(f'os dados obtidos de {file.name} são inválidos')
            return
        
        # transformar os dados do contexto num objeto
        try:
            context = Context.from_dict(
                data=data,
                file=file,
                active_root=active_root
            )
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