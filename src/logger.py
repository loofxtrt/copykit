from rich.console import Console, Group
from rich.text import Text
from rich.markup import escape
from rich.panel import Panel
from rich.live import Live


class EntryLogger():
    def __init__(self, title: str):
        self.title = title
        self.messages = []

        self.console = Console()

        self.live = Live(
            self._render_panel(),
            console=self.console,
            refresh_per_second=10
        )
        self.live.start()

    def _render_panel(self):
        return Panel(
            Group(*self.messages),
            title=self.title
        )
    
    def _handle_message(self, message):
        textified = Text(f'    {message}')
        self.messages.append(textified)
        self.live.update(self._render_panel())

    def close(self):
        self.live.stop()

    def warning(self, message):
        self._handle_message(message)

    def error(self, message):
        self._handle_message(message)

    def info(self, message):
        self._handle_message(message)

    def skip(self, message):
        self._handle_message(message)

    def success(self, message):
        self._handle_message(message)

    def symlink(self, message):
        self._handle_message(message)

    def debug(self, message):
        self._handle_message(message)

    def critical(self, message):
        self._handle_message(message)


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