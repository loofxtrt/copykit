from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
import json

from .globals import PACK_LOCAL, PACK_REMOTE, SUBSTITUTES, INSTRUCTIONS, normalize_json_name, normalize_svg_name, read_json, write_json
from . import logger


@dataclass
class Context:
    """
    define o contexto base para resolução de caminhos e identificação do mapping

    args:
    	id:
    		identificador usado principalmente pra logs
            NÃO precisa ser idêntico ao nome do arquivo json que contém ele

    	data:
            dados brutos do CONTEXTO. isso NÃO inclui um mapping inteiro,
            só a parte que fica contida dentro da chove context
        
        active_root:
            raíz do icon pack alvo

        target_parent:
            raíz onde os targets devem começar a serem procurados
            se o target for 'blender' e o target_parent for 'apps/scalable',
            apps/scalable vai ser varrido até encontrar apps/scalable/blender.svg
        
        substitute_parent:
            mesma lógica do target_parent, mas pros substitutos
            'novo-blender', 'substitutos' -> substitutos/blender.svg
    """

    id: str
    data: dict
    active_root: Optional[Path]
    target_parent: Optional[Path] = field(init=False)
    substitute_parent: Optional[Path] = field(init=False)

    def __post_init__(self):
        # TODO: erros melhores nos dois
        # TODO: wrapper intermediário pros dois?
        self.target_parent = self._resolve_target_parent()
        self.substitute_parent = self._resolve_substitute_parent()

    @classmethod
    def from_dict(
        cls,
        data: dict,
        file: Path,
        active_root: Path | None = None
        ) -> Context:
        """
        resolve e valida o contexto a partir dos dados carregados de um json

        args:
            file:
                caminho do arquivo json que contém os dados
                só é usado para mensagens de erro enquanto o id do mapping não for resolvido
        """

        _id = data.get('id')
        if not _id:
            raise ValueError(f'id não definido ({file.name})')
        
        return cls(
            id=_id,
            data=data,
            active_root=active_root
        )
    
    def _resolve_target_parent(self) -> Path | None:
        # obter o parent do target e resolver o path
        if not self.active_root:
            return None
        
        raw = self.data.get('target_parent')

        if not raw:
            return None

        if 'ROOT' not in raw:
            raise ValueError(f"'ROOT' precisa estar presente em target_parent ({self.id})")
        
        return Path(raw.replace('ROOT', str(self.active_root)))

    def _resolve_substitute_parent(self) -> Path | None:
        # obter o parent do substituto e resolver o path
        # TODO: fazer SUBSTITUTES ser param
        raw = self.data.get('substitute_parent')
        
        if not raw:
            return None
        
        if 'SUBSTITUTES' not in raw:
            raise ValueError(f"'SUBSTITUTES' precisa estar presente em substitute_parent ou ser completamente nulo ({self.id})")
        
        return Path(raw.replace('SUBSTITUTES', str(SUBSTITUTES)))
    
    def to_dict(self) -> dict:
        # return {
        #     'id': self.id,
        #     'substitute_parent': self.substitute_parent,
        #     'target_parent': self.target_parent
        # }
        return self.data


@dataclass
class Target:
    """
    representa um arquivo de destino que sofrerá alguma ação (create, replace, symlink ou remove)

    args:
    	icon:
    		nome lógico do ícone, usado para identificação e construção do caminho

    	action:
    		ação que será aplicada ao target. pode ser:
            - create, replace
                na prática não têm diferença. create só serve pra deixar claro
                que um ícone não existia no pack original e foi criado sobre ele

            - symlink
                cria um symlink apontando pra um outro arquivo já existente. não requer substitute
                isso requer um canonical previamente definido na Entry que possui esse Target
            
            - remove
                deleta um arquivo. não requer substitute
    """
    
    icon: str # equivalente à name, TODO: talvez mudar pra name
    action: str

    def resolve_path(self, context: Context) -> Path | None:
        if not context.target_parent:
            logger.error(f'não é possível resolver o caminho do target sem um target_parent: {context.id}')
            return
        
        return context.target_parent / normalize_json_name(self.icon)

    def to_dict(self) -> dict:
        return {
            'icon': self.icon,
            'action': self.action
        }


@dataclass
class Substitute: # TODO: trocar substitute pra substitute_name no json? provavelmente não
    """
    representa um arquivo substituto que será usado em operações de create ou replace

    args:
    	name:
    		nome lógico do substituto, vindo do json
    """

    name: str

    def resolve_path(self, context: Context) -> Path | None:
        if not context.substitute_parent:
            logger.error(f'não é possível resolver o caminho do substitute sem um substitute_parent: {context.id}')
            return
        
        return context.substitute_parent / normalize_json_name(self.name)


@dataclass
class Entry:
    """
    agrupa um substituto opcional com uma lista de targets que compartilham esse substituto

    args:
    	substitute:
    		substituto associado aos targets,
            pode ser nulo para ações que não precisam dele, tipo remoções ou criação de symlinks

    	targets:
    		lista de targets que serão processados
        
        canonical:
            pra onde o symlink deve apontar. só é necessário se a action do target for 'symlink'
            isso geralmente deve ser um caminho relativo, tipo 'blender.svg' ou '../blender.svg'

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
    sources: Optional[list[dict]]
    processing: Optional[str]

    @classmethod
    def from_dict(
        cls,
        data: dict,
        key: str,
        context: Context
        ) -> Entry | None:
        # resolver o substitute
        substitute = Substitute(name=data.get('substitute'))
        
        # resolver os targets
        targets = []
        for raw_target in data.get('targets', []):
            icon = raw_target.get('icon')
            action = raw_target.get('action')

            if not icon or not action:
                logger.error(f'target inválido em {context.id}')
                continue
            
            # resolver o path completo do target com base no contexto
            target_parent = context.target_parent
            path = None
            if target_parent:
                path = context.target_parent / normalize_svg_name(icon)

            # adicionar o target resolvido à lista
            targets.append(
                Target(icon=icon, action=action)
            )

        return cls(
            key=key,
            substitute=substitute,
            targets=targets,
            canonical=data.get('canonical'),
            changelog=data.get('changelog'),
            sources=data.get('sources', []),
            processing=data.get('processing')
        )

    def insert_target(self, target: Target):
        self.targets.append(target)
    
    def insert_source(self, source: str, assets: list[str] | None = None, used: str | None = None):
        data = {
            'source': source
        }

        if assets:
            data['assets'] = assets
        if used:
            data['used'] = used
        
        self.sources.append(data)

    def to_dict(self) -> dict:
        targets = []
        for t in self.targets:
            targets.append(t.to_dict())
        
        data = {
            'substitute': self.substitute.name if self.substitute else None,
            'targets': targets,
            'canonical': self.canonical,
            'changelog': self.changelog,
            'sources': self.sources,
            'processing': self.processing
        }

        return {
            # TODO: func separada?
            k: v for k, v in data.items() if v is not None
        }


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
    def from_file(
        cls,
        file: Path,
        active_root: Path | None = None
        ) -> Mapping | None:
        """
        converte um arquivo json em um objeto mapping estruturado

        args:
            file:
                caminho do arquivo json contendo instruções
        """

        if not file.is_file():
            raise ValueError(f'{file.resolve} não é um arquivo válido')
        
        data = read_json(file)
        if not data:
            logger.error(f'os dados obtidos de {file.name} são inválidos')
            return
        
        # transformar os dados do contexto num objeto
        try:
            context = Context.from_dict(
                data=data.get('context'),
                file=file,
                active_root=active_root
            )
        except ValueError as err:
            logger.error(f'erro ao resolver o contexto de {file.name}: {err}')
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

        # criar o mapping
        mapping = Mapping(
            context=context,
            entries=entries
        )
        return mapping
    
    def to_dict(self) -> dict:
        entries = {}
        for key, value in self.entries.items():
            entries[key] = value.to_dict()

        return {
            'context': self.context.to_dict(),
            'entries': entries
        }
    
    def insert_entry(self, key: str, entry: Entry):
        self.entries[key] = entry
    
    def save_to_disk(self, file: Path):
        """
        transforma o estado atual da classe em texto
        e escreve no disco, substituindo o conteúdo anterior
        """

        write_json(file, self.to_dict())