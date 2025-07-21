import argparse
from pathlib import Path

from src import fetch, replace
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED, SUBSTITUTES_APPS

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

        fetch.fetch(search_terms=terms, input_dir=ORIGINAL_UNZIPPED, output_dir=FETCH_OUTPUT)
    elif args.mode == "fetch" and args.clear:
        fetch.clear(output_dir=FETCH_OUTPUT)
    
    if args.mode == "replace":
        replace_map = {
            "discord": {
                "substitute": SUBSTITUTES_APPS / "kora_discord.svg",
                "aliases": [
                    "discord",
                    "discord-bin",
                    "discord-ptb", 
                    "solstice-discord-discord",
                    "com.discordapp.Discord",
                ],
            },
            "discord-canary": {
                "substitute": SUBSTITUTES_APPS / "kora_discord-canary.svg",
                "aliases": [
                    "discord-canary",
                    "com.discordapp.DiscordCanary",
                ],
            },
            "discord-development": {
                "substitute": SUBSTITUTES_APPS / "kora_discord-development.svg",
                "aliases": [
                    "discord-development",
                ],
            },
            "spotify": {
                "substitute": SUBSTITUTES_APPS / "marwaita_spotify.svg",
                "aliases": [
                    "com.spotify.Client",
                    "nuvolaplayer3_spotify",
                    "spotify",
                    "spotify-client",
                    "solstice-spotify-spotify",
                    "spotify-qt",
                ],
            },
            "obs": {
                "substitute": SUBSTITUTES_APPS / "kora_obs.svg",
                "aliases": [
                    "com.obsproject.Studio",
                    "obs",
                ],
            },
            "krita": {
                "substitute": SUBSTITUTES_APPS / "marwaita_krita.svg",
                "aliases": [
                    "calligrakrita",
                    "calligrakrita2",
                    "org.kde.krita",
                ],
            },
            "gimp": {
                "substitute": SUBSTITUTES_APPS / "breeze-dark_gimp.svg",
                "aliases": [
                    "gimp",
                    "org.gimp.GIMP",
                ],
            },
            "godot": {
                "substitute": SUBSTITUTES_APPS / "plasmax_godot.svg",
                "aliases": [
                    "godot",
                    "godot-mono",
                    "lutris_godot-engine",
                    "org.godotengine.Godot",
                    "org.godotengine.Godot3",
                ],
            },
            "inkscape": {
                "substitute": SUBSTITUTES_APPS / "plasmax_inkscape.svg",
                "aliases": [
                    "inkscape",
                    "inkscape-logo",
                    "org.inkscape.Inkscape",
                ],
            },
            "blender": {
                "substitute": SUBSTITUTES_APPS / "blender.svg",
                "aliases": [
                    "org.blender.Blender",
                ],
            },
            "obsidian": {
                "substitute": SUBSTITUTES_APPS / "kora_obsidian.svg",
                "aliases": [
                    "md.obsidian.Obsidian",
                    "obsidian",
                    "appimagekit-obsidian",
                ],
            },
            "steam": {
                "substitute": SUBSTITUTES_APPS / "marwaita_steam.svg",
                "aliases": [
                    "steam",
                    "steam-icon",
                    "steam-launcher",
                    "steamos-logo-icon",
                    "steampowered",
                    "steamskinmanager",
                ],
            },
            "libresprite": {
                "substitute": SUBSTITUTES_APPS / "libresprite.svg",
                "aliases": [
                    "com.github.libresprite.LibreSprite"
                ],
            },
            "aseprite": {
                "substitute": SUBSTITUTES_APPS / "aseprite.svg",
                "aliases": [
                    "lutris_aseprite"
                ],
            },
            "pureref": {
                "substitute": SUBSTITUTES_APPS / "kora_pureref.svg",
                "aliases": [

                ],
            },
            "endeavouros": {
                "substitute": SUBSTITUTES_APPS / "endeavouros.svg",
                "aliases": [
                    "distributor-logo-endeavouros",
                    "endeavouros",
                    "endeavouros-icon"
                ],
            },
            "sqlitebrowser": {
                "substitute": SUBSTITUTES_APPS / "sqlitebrowser.svg",
                "aliases": [
                    "org.sqlitebrowser.sqlitebrowser",
                ],
            },
            "vinegar": {
                "substitute": SUBSTITUTES_APPS / "vinegar.svg",
                "aliases": [
                    "io.github.vinegarhq.Vinegar",
                    "org.vinegarhq.Vinegar"
                ],
            },
            "roblox": {
                "substitute": SUBSTITUTES_APPS / "roblox.svg",
                "aliases": [
                    "io.github.vinegarhq.Vinegar.player"
                ],
            },
            "roblox-studio": {
                "substitute": SUBSTITUTES_APPS / "roblox-studio.svg",
                "aliases": [
                    "io.github.vinegarhq.Vinegar.studio"
                ],
            },
            "sober": {
                "substitute": SUBSTITUTES_APPS / "sober.svg",
                "aliases": [
                    "org.vinegarhq.Sober"
                ],
            },
            "audacity": {
                "substitute": SUBSTITUTES_APPS / "reversal-black_audacity.svg",
                "aliases": [
                    "org.audacityteam.Audacity",
                    "application-x-audacity-project",
                    "audacity16",
                    "audacity32"
                ],
            },
            "vscodium": {
                "substitute": SUBSTITUTES_APPS / "codium.svg",
                "aliases": [
                    "com.vscodium.codium",
                ],
            }
        }

        destinations = [
            Path("/home/luan/.local/share/icons/coral"),
            Path("/home/luan/.local/share/icons/coral-light"),
            Path("/home/luan/.local/share/icons/coral-light-panel"),
        ]

        # obter os valores do replace_map, ignorando a chave e obtendo apenas os valores das entradas
        # então, pra cada 
        for _, entry in replace_map.items():
            replace.replace(
                target_names=entry["aliases"],
                substitute_file=entry["substitute"],
                destinations_dirs=destinations
            )
main()