import sys
from pathlib import Path
from xml.dom import minidom
from yattag import Doc

from .models import Mapping
from .globals import INSTRUCTIONS, PACK_REPO, README_TEMPLATE


def make_hyperlink(url: str, text: str) -> str:
    return f'[{text}]({url})'

def resolve_table_writing(mapping: Mapping):
    doc, tag, text = Doc().tagtext()

    map_id = mapping.context.id
    map_entries = mapping.entries.values()

    # criar o campo expansível com a tabela
    with tag('details'):
        with tag('summary'):
            text(f'{map_id} (click to expand)')

        with tag('table'):
            # cabeçalho
            with tag('tr'):
                for header in ['Entry', 'Source', 'Changes']:
                    with tag('th'): text(header)

            # criar um table row pra cada entrada do array de dicts
            for e in map_entries:
                with tag('tr'):
                    # obter os valores primários
                    key = e.key
                    sources = e.sources
                    changelog = e.changelog

                    # formatar as sources
                    sources_text = ''
                    if sources:
                        for s in sources:
                            source = s.get('source')
                            assets = s.get('assets')
                            used = s.get('used')

                            sources_text += f'@source: `{source}` assets: `{str(assets)}` used: `{used}`'

                    with tag('td'):
                        text(key)

                    # doc.asis insere html dentro do html sem precisar escapar
                    with tag('td'):
                        doc.asis(sources_text)
                    with tag('td'):
                        doc.asis(changelog or '')

    # renderizar a tabela e retornar
    raw_html = doc.getvalue()
    pretty_html = minidom.parseString(raw_html).toprettyxml()

    return pretty_html

def run_documenter():
    ICON_PACKS = {
        'KORA': make_hyperlink('https://store.kde.org/p/1256209', 'Kora'),
        'BREEZE': make_hyperlink('https://github.com/KDE/breeze-icons', 'Breeze'),
        'MARWAITA': make_hyperlink('https://www.gnome-look.org/p/1239855', 'Marwaita'),
        'MOREWAITA': make_hyperlink('https://www.gnome-look.org/p/2276064', 'MoreWaita'),
        'PLASMAX': make_hyperlink('https://www.gnome-look.org/p/1367155', 'PlasmaX'),
        'INFINITY': make_hyperlink('https://www.gnome-look.org/p/2112373', 'Infinity'),
        'REVERSAL': make_hyperlink('https://www.gnome-look.org/p/1340791', 'Reversal'),
        'FLAT_REMIX': make_hyperlink('https://store.kde.org/p/1012430', 'Flat Remix'),
        'FAIRYWREN': make_hyperlink('https://www.gnome-look.org/p/1684521', 'FairyWren'),
        'YOSA_MAX': make_hyperlink('https://www.gnome-look.org/p/1196255/', 'Yosa Max'),
        'PAPIRUS': make_hyperlink('https://www.gnome-look.org/p/1166289/', 'Papirus'),
        'QOGIR': make_hyperlink('https://github.com/vinceliuice/Qogir-icon-theme', 'Qogir'),
        'FLUENT': make_hyperlink('https://store.kde.org/p/1477945', 'Fluent'),
    }

    # ler o conteúdo base
    with README_TEMPLATE.open('r', encoding='utf-8') as f:
        base = f.read()

    # criar as tabelas
    tables = []
    for f in INSTRUCTIONS.rglob('*.json'):
        mapping = resolve_table_writing(Mapping.from_file(f))
        tables.append(mapping)
    
    # substituir os placeholders do template
    resolved = base.replace(
        '{TABLES}',
        '\n'.join(tables)
    )

    resolved = resolved.replace(
        '{ICON_PACKS}',
        ', '.join(ICON_PACKS.values())
    )

    resolved = resolved.replace(
        'SCRATCH',
        'made from scratch'
    )

    # readme = PACK_REPO / 'README.md'
    readme = Path('/mnt/seagate/workspace/coding/projetos/scripts/copykit/teste.md')
    with open(readme, 'w') as f:
        f.write(resolved)

# TODO: adicionar o "from scratch", formatar melhor as sources pra não serem só uma list com str
# TODO: fazer os templates dos json também serem envoltos em {} pra diferenciar melhor de texto comum