import inspect
from pathlib import Path

from src.utils.paths import ROOT

RESET = "\033[0m"

GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"

color_map = {
    "success": GREEN,
    "error": RED,
    "warning": YELLOW,
    "info": BLUE,
    "debug": GREEN
}

def get_caller_name():
    """
        inspeciona qual foi a função responsável por chamar esta,  
        subindo quantos níveis de hierarquia forem necessários
    """

    stack = inspect.stack()
    
    try:
        # num exemplo do uso do success, a lógica e ordem é:
        # chamador real (quem chamou o success) -> success -> base -> get_caller_name
        caller_frame = stack[3].frame

        # obter as informações desse frame assim que ele for identificado
        caller_name = caller_frame.f_code.co_name
        file_name = Path(caller_frame.f_code.co_filename)
        lineno = caller_frame.f_lineno

        # encurtar o caminho absoluto pra relativo
        file_name = file_name.relative_to(ROOT)

        return caller_name, file_name, lineno
    finally:
        # deletar o stack após terminar o uso
        del stack

def base(level, msg):
    caller_name, file_name, lineno = get_caller_name()

    # definir a cor com base no color map de levels
    if level in color_map:
        color = color_map[level]
    else:
        color = RESET

    # formatar as linhas
    level = (f"{color}{level.upper()}{RESET}")
    final = f"[ {level} - {file_name}:{lineno}:{caller_name} ] {msg}"
    
    print(final)

def success(msg):
    base("success", msg)

def error(msg):
    base("error", msg)

def info(msg):
    base("info", msg)

def debug(msg):
    base("debug", msg)

def warning(msg):
    base("warning", msg)