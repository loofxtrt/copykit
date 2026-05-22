import sys
from pathlib import Path
from xml.dom import minidom
from yattag import Doc

from .replacer import Mapping, resolve_mapping
from .globals import INSTRUCTIONS, PACK_REPO


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

                    with tag('td'):
                        text(key)

                    # doc.asis insere html dentro do html sem precisar escapar
                    with tag('td'):
                        doc.asis(str(sources) or '')
                    with tag('td'):
                        doc.asis(changelog or '')

    # renderizar a tabela e retornar
    raw_html = doc.getvalue()
    pretty_html = minidom.parseString(raw_html).toprettyxml()

    return pretty_html

def run_documenter():
    kora       = make_hyperlink('https://store.kde.org/p/1256209', 'Kora')
    breeze     = make_hyperlink('https://github.com/KDE/breeze-icons', 'Breeze')
    marwaita   = make_hyperlink('https://www.gnome-look.org/p/1239855', 'Marwaita')
    morewaita  = make_hyperlink('https://www.gnome-look.org/p/2276064', 'MoreWaita')
    plasma_x   = make_hyperlink('https://www.gnome-look.org/p/1367155', 'PlasmaX')
    infinity   = make_hyperlink('https://www.gnome-look.org/p/2112373', 'Infinity')
    reversal   = make_hyperlink('https://www.gnome-look.org/p/1340791', 'Reversal')
    flat_remix = make_hyperlink('https://store.kde.org/p/1012430', 'Flat Remix')
    fairywren  = make_hyperlink('https://www.gnome-look.org/p/1684521', 'FairyWren')
    yosa_max   = make_hyperlink('https://www.gnome-look.org/p/1196255/', 'Yosa Max')
    papirus    = make_hyperlink('https://www.gnome-look.org/p/1166289/', 'Papirus')
    qogir      = make_hyperlink('https://github.com/vinceliuice/Qogir-icon-theme', 'Qogir')
    fluent     = make_hyperlink('https://store.kde.org/p/1477945', 'Fluent')
    scratch    = 'made from scratch'

    FIRST_CHUNK = f'''
<img src="./copycat_banner.svg" width="256" alt="Copycat" style="display: block;">
An icon theme forked from Kora, replacing/modifying a few icons while trying to make them more accurate to the original software logo's colors and shapes  
  
All folder icons were regenerated using Copyhex to fix small inconsistencies in gradients and change glyphs  
  
[![Static Badge](https://img.shields.io/badge/tar.gz-download_icon_pack-yellow)](https://github.com/loofxtrt/copycat/releases/latest)  
  
## Credits
Icons from different packs are included in this repo, **all licensed under the GPL3 license**  
Those packs includes:  
{kora}, {breeze}, {marwaita}, {morewaita}, {plasma_x}, {infinity}, {reversal}, {flat_remix}, {fairywren}, {yosa_max}, {papirus}, {qogir}, {fluent}

## Major differences
'''

    LAST_CHUNK = '''
## License
[GPL3](https://www.gnu.org/licenses/gpl-3.0-standalone.html)
'''

    # criar as tabelas
    tables = []
    for f in INSTRUCTIONS.rglob('*.json'):
        mapping = resolve_table_writing(Mapping.from_file(f))
        tables.append(mapping)
    
    # condensar as informações junto com as tabelas em uma só string
    # e depois escrever o arquivo markdown final
    condensed = FIRST_CHUNK
    for t in tables:
        condensed += t
    condensed += LAST_CHUNK

    readme = PACK_REPO / 'README.md'
    with open(readme, 'w') as f:
        f.write(condensed)

# TODO: adicionar o "from scratch", formatar melhor as sources pra não serem só uma list com str
run_documenter()