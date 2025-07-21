import argparse
from pathlib import Path

from src import fetch
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED

def set_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="fetch/replace")
    parser.add_argument("--clear", "-c", action="store_true", help="limpa o diretório de output")

    return parser

def main():
    parser = set_parser()
    args = parser.parse_args()

    if args.mode == "fetch" and not args.clear:
        terms = [
            "appimagelauncher",
            "btop",
            "kvantum",
            "pureref",
            "davinci"
        ]

        for t in terms:
            fetch.fetch(search_term=t, input_dir=ORIGINAL_UNZIPPED, output_dir=FETCH_OUTPUT)
    elif args.mode == "fetch" and args.clear:
        fetch.clear(output_dir=FETCH_OUTPUT)

main()