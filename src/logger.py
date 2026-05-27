from rich.console import Console, Group
from rich.text import Text
from rich.markup import escape
from rich.panel import Panel
from rich.live import Live
from rich.style import Style


COLOR_MAP = {
        'warning': 'yellow',
        'info': 'default',
        'debug': 'cyan',
        'error': 'red',
        'success': 'green',
        'symlink': 'blue',
        'normal': 'default'
    }


class EntryLogger():
    def __init__(self, title: str, prefix: str | None = None):
        """
        args:
            title:
                título principal do painel
            
            prefix:
                prefixo opcional que vem antes do título
                ex: 'lorem:' -> lorem:ipsum
        """

        self.title = title
        self.prefix = prefix
        self.messages = []

        self.console = Console()

        # cria o ambiente vivo
        # IMPORTANTE: deve ser manualmente parado quando o logger for morto
        # se não bugs acontecem. ex: logs cortados por outros
        self.live = Live(
            self._render_panel(),
            console=self.console,
            refresh_per_second=10
        )
        self.live.start()

    def _render_panel(self, level: str | None = None):
        """
        renderiza um painel representando o estado atual do logger
        baseado em todas as mensagens salvas na memória
        
        args:
            level:
                o nível da última mensagem que foi passada pro logger
                é usado pra redefinir a cor da borda do painel enquanto ele acontece
                
                pode ser none porque ele precisa ser chamado no init, que não passa um level
        """

        # formatar o título e adicionar o prefixo se ele existir
        title = Text()
        
        if self.prefix:
            title.append(self.prefix)
        
        title.append_text(Text(self.title, style='bold'))

        return Panel(
            Group(*self.messages), # desempacota lista de mensagens uma por uma
            title=title,
            border_style=get_level_color(level),
            title_align='left'
        )
    
    def _handle_message(self, message: str, level: str):
        """
        formata uma nova mensagem, insere ela na memória
        e renderiza o estado atual do logger
        """

        formatted = format_message(message, level)
        self.messages.append(formatted)

        self.live.update(self._render_panel(level))

    def close(self):
        """
        termina o ambiente vivo quando ele não for mais necessário
        chamar isso é responsabilidade de quem criou uma instância dessa classe
        """

        self.live.stop()

    def warning(self, message):
        self._handle_message(message, 'warning')

    def error(self, message):
        self._handle_message(message, 'error')

    def info(self, message):
        self._handle_message(message, 'info')

    def success(self, message):
        self._handle_message(message, 'success')

    def symlink(self, message):
        self._handle_message(message, 'symlink')

    def debug(self, message):
        self._handle_message(message, 'debug')


def get_level_color(level: str | None) -> str:
    """
    obtém a cor equivalente a um nível de logging
    se nenhum nível foi passado, se assume que é um texto normal
    """

    return COLOR_MAP.get(level.lower() if level else '', 'normal')

def format_message(
    message: str,
    level: str,
    level_bold: bool = False,
    level_upper: bool = False,
    ) -> Text:
    """
    formata uma mensagem de log em um objeto Text do rich

    args:
        message:
            texto da mensagem de log

        level:
            nível da mensagem de log (ex: 'info', 'error', 'warning').
            é usado para definir cor e rotular cada mensagem

        level_bold:
            se deve ou não aplicar negrito no texto do level

        level_upper:
            se deve ou não passar o texto do level pra UPPERCASE
    """

    color = get_level_color(level)
    
    # identificar o level mais longo possível
    # pra ajustar o padding de acordo com ele
    longest = max(COLOR_MAP.keys(), key=len)
    
    # estilizar o texto do level
    level_text = level.upper() if level_upper else level
    level_text = level_text.ljust(len(longest))
    level_style = Style(color=color, bold=level_bold)

    # construir o texto final
    text = Text()
    text.append_text(
        Text(level_text, level_style)
    )
    text.append(' ')
    text.append_text(
        Text(message, overflow='fold')
    )

    return text

# TODO: extinguir esse logger antigo
def message_formatter(message, level: str = 'info', with_background: bool = False):
    lvl_colors = {
        'warning': 'yellow',
        'info': 'blue',
        'debug': 'green',
        'error': 'red',
        'critical': 'red',
        'success': 'green',
        'skip': 'blue',
        'symlink': 'blue'
    }

    # formatar o indicador de level
    # usa o level passado pra essa função, em lowercase, pra obter a cor do indicador
    # na hora de imprimir, sempre mostra o level em uppercase
    # se o with_background estiver presente, adiciona isso (mas só pra primeira linha, pro resto não)
    color = lvl_colors.get(level.lower(), 'blue')
    
    level = level.upper()
    if with_background:
        # caso tenhha background, adicionar padding extra e o background em si
        level_display = f' {level} '
        handle_color = f'black on {color}'
    else:
        level_display = level
        handle_color = color
    
    handle_color += ' bold'
    lvl_indicator = Text(level_display, handle_color)

    # iniciar a formatação da mensagem
    # escape é usado pra que o rich não reconheça caracteres do texto como parte da formatação
    # str é usado pra garantir que qualquer coisa seja printável
    message = escape(str(message))
    formatted = Text()

    # se a mensagem tiver mais de uma linha, tratar essas linhas extras
    lines = message.splitlines()
    
    if len(lines) > 0:
        # adiciona a primeira linha de todas com a cor normal
        # ao lado do indicador de level
        formatted.append(lines[0])

        # verifica as demais linhas, começando do índice 1
        # pq o índice zero já foi adicionado como primeira linha
        for l in lines[1:]:
            formatted.append(f'\n   {l}')

    panel = Panel(
        formatted,
        title=lvl_indicator,
        title_align='left',
        border_style=color
    )

    console = Console()
    console.print(panel)

def warning(message):
    message_formatter(message=message, level='warning')

def error(message):
    message_formatter(message=message, level='error')

def info(message):
    message_formatter(message=message, level='info')

def skip(message):
    message_formatter(message=message, level='skip')

def success(message):
    message_formatter(message=message, level='success')

def symlink(message):
    message_formatter(message=message, level='symlink')

def debug(message):
    message_formatter(message=message, level='debug', with_background=True)

def critical(message):
    message_formatter(message=message, level='critical', with_background=True)