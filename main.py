import argparse
from pathlib import Path

from src import fetch, replace
from src.utils.paths import FETCH_OUTPUT, ORIGINAL_UNZIPPED, SUBSTITUTES_APPS, SUBSTITUTES_SYSTEM, SUBSTITUTES_PLACES

def set_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="fetch/replace")
    parser.add_argument("--section", "-s", help="software/system, seção à qual o replace deve ser aplicado")
    parser.add_argument("--replacelevel", "-rl", help="repo/local, se presente, define se só o repo ou o local vai ser atualizado. se não, atualiza os dois")
    parser.add_argument("--clear", "-c", action="store_true", help="limpa o diretório de output")

    return parser

def main():
    parser = set_parser()
    args = parser.parse_args()

    if args.mode == "fetch" and not args.clear:
        terms = [
            # "appimagelauncher",
            # "btop",
            # "ark",
            # "kvantum",
            # "pureref",
            # "davinci",
            # "settings",
            # "folder",
            # "archive",
            # "arca",
            # "android",
            # "btop",
            # "monitor",
            # "dolphin",
            # "gcolor3",
            # "nl.hjdskes.gcolor3",
            # "picker",
            # "cmake",
            "firewall"
        ]

        fetch.fetch(search_terms=terms, input_dir=ORIGINAL_UNZIPPED, output_dir=FETCH_OUTPUT)
    elif args.mode == "fetch" and args.clear:
        fetch.clear(output_dir=FETCH_OUTPUT)
    
    if args.mode == "replace":
        if args.section == "software":
            replace_map = {
                "discord": {
                    "substitute": SUBSTITUTES_APPS / "kora_discord.svg",
                    "aliases": [
                        "discord",
                        "discord-bin",
                        "discord-ptb", 
                        "solstice-discord-discord",
                        "com.discordapp.Discord",
                    ]
                },
                "discord-canary": {
                    "substitute": SUBSTITUTES_APPS / "kora_discord-canary.svg",
                    "aliases": [
                        "discord-canary",
                        "com.discordapp.DiscordCanary",
                    ]
                },
                "discord-development": {
                    "substitute": SUBSTITUTES_APPS / "kora_discord-development.svg",
                    "aliases": [
                        "discord-development",
                    ]
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
                    ]
                },
                "obs": {
                    "substitute": SUBSTITUTES_APPS / "kora_obs.svg",
                    "aliases": [
                        "com.obsproject.Studio",
                        "obs",
                    ]
                },
                "krita": {
                    "substitute": SUBSTITUTES_APPS / "marwaita_krita.svg",
                    "aliases": [
                        "calligrakrita",
                        "calligrakrita2",
                        "org.kde.krita",
                    ]
                },
                "gimp": {
                    "substitute": SUBSTITUTES_APPS / "breeze-dark_gimp.svg",
                    "aliases": [
                        "gimp",
                        "org.gimp.GIMP",
                    ]
                },
                "godot": {
                    "substitute": SUBSTITUTES_APPS / "plasmax_godot.svg",
                    "aliases": [
                        "godot",
                        "godot-mono",
                        "lutris_godot-engine",
                        "org.godotengine.Godot",
                        "org.godotengine.Godot3",
                    ]
                },
                "inkscape": {
                    "substitute": SUBSTITUTES_APPS / "plasmax_inkscape.svg",
                    "aliases": [
                        "inkscape",
                        "inkscape-logo",
                        "org.inkscape.Inkscape",
                    ]
                },
                "blender": {
                    "substitute": SUBSTITUTES_APPS / "blender.svg",
                    "aliases": [
                        "org.blender.Blender",
                    ]
                },
                "obsidian": {
                    "substitute": SUBSTITUTES_APPS / "kora_obsidian.svg",
                    "aliases": [
                        "md.obsidian.Obsidian",
                        "obsidian",
                        "appimagekit-obsidian",
                    ]
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
                    ]
                },
                "libresprite": {
                    "substitute": SUBSTITUTES_APPS / "libresprite.svg",
                    "aliases": [
                        "com.github.libresprite.LibreSprite"
                    ]
                },
                "aseprite": {
                    "substitute": SUBSTITUTES_APPS / "aseprite.svg",
                    "aliases": [
                        "lutris_aseprite"
                    ]
                },
                "pureref": {
                    "substitute": SUBSTITUTES_APPS / "kora_pureref.svg",
                },
                "endeavouros": {
                    "substitute": SUBSTITUTES_APPS / "endeavouros.svg",
                    "aliases": [
                        "distributor-logo-endeavouros",
                        "endeavouros",
                        "endeavouros-icon"
                    ]
                },
                "sqlitebrowser": {
                    "substitute": SUBSTITUTES_APPS / "sqlitebrowser.svg",
                    "aliases": [
                        "org.sqlitebrowser.sqlitebrowser",
                    ]
                },
                "vinegar": {
                    "substitute": SUBSTITUTES_APPS / "vinegar.svg",
                    "aliases": [
                        "io.github.vinegarhq.Vinegar",
                        "org.vinegarhq.Vinegar"
                    ]
                },
                "roblox": {
                    "substitute": SUBSTITUTES_APPS / "roblox.svg",
                    "aliases": [
                        "io.github.vinegarhq.Vinegar.player"
                    ]
                },
                "roblox-studio": {
                    "substitute": SUBSTITUTES_APPS / "roblox-studio.svg",
                    "aliases": [
                        "io.github.vinegarhq.Vinegar.studio"
                    ]
                },
                "sober": {
                    "substitute": SUBSTITUTES_APPS / "sober.svg",
                    "aliases": [
                        "org.vinegarhq.Sober"
                    ]
                },
                "audacity": {
                    "substitute": SUBSTITUTES_APPS / "reversal-black_audacity.svg",
                    "aliases": [
                        "org.audacityteam.Audacity",
                        "application-x-audacity-project",
                        "audacity16",
                        "audacity32"
                    ]
                },
                "vscodium": {
                    "substitute": SUBSTITUTES_APPS / "codium.svg",
                    "aliases": [
                        "com.vscodium.codium",
                    ]
                },
                "appimagelauncher": {
                    "substitute": SUBSTITUTES_APPS / "flat-remix-blue-dark_appimagelauncher.svg",
                    "aliases": [
                        "AppImageLauncher"
                    ]
                },
                "android-studio": {
                    "substitute": SUBSTITUTES_APPS / "fairywren_dark_android-studio.svg",
                    "aliases": [
                        "android-studio-beta"
                    ]
                },
                "android-studio-canary": {
                    "substitute": SUBSTITUTES_APPS / "fairywren_dark_android-studio-canary.svg"
                },
                "btop": {
                    "substitute": SUBSTITUTES_APPS / "kora_btop.svg"
                },
                "ark": {
                    "substitute": SUBSTITUTES_APPS / "yosa-max_ark.svg",
                    "aliases": [
                        "org.kde.ark",
                        "accessories-archiver",
                        "archive-manager",
                        "archivemanager",
                        "gvfsd-archive-file",
                        "lxqt-archiver",
                        "org.gnome.ArchiveManager",
                        "utilities-file-archiver",
                        "xarchiver"
                    ]
                },
                "dolphin": {
                    "substitute": SUBSTITUTES_APPS / "kora_dolphin.svg",
                    "aliases": [
                        "org.kde.dolphin"
                    ]
                },
                "github-desktop": {
                    "substitute": SUBSTITUTES_APPS / "kora_github-desktop.svg",
                    "aliases": [
                        "appimagekit-github-desktop",
                        "io.github.shiftey.Desktop"
                    ]
                },
                "color-picker": {
                    "substitute": SUBSTITUTES_APPS / "marwaita_color-picker.svg",
                    "aliases": [
                        "gcolor3",
                        "nl.hjdskes.gcolor3"
                    ]
                },
                "kvantum": {
                    "substitute": SUBSTITUTES_APPS / "kora_kvantum.svg"
                },
                "fspy": {
                    "substitute": SUBSTITUTES_APPS / "kora_fspy.svg",
                    "aliases": [
                        "appimagekit-fspy",
                        "appimagekit_7b72cc93eb7f580b01420d811fd0cc64_fspy"
                    ]
                },
                "cmake": {
                    "substitute": SUBSTITUTES_APPS / "kora_cmake.svg",
                    "aliases": [
                        "cmake",
                        "cmake-gui",
                        "CMakeSetup",
                        "CMakeSetup32"
                    ]
                }
            }
        elif args.section == "system":
            replace_map = {
                "settings": {
                    "substitute": SUBSTITUTES_SYSTEM / "reversal-black_cosmic-settings.svg",
                    "aliases": [
                        "computersettings",
                        "org.xfce.settings.manager",
                        "redhat-system_settings",
                        "com.system76.CosmicSettings",
                        "package-settings",
                        "systemsettings",
                        "gnome-settings",
                        "package_settings",
                        "xfce4-settings",
                        "org.gnome.Settings",
                        "redhat-server_settings",
                        "xfce-system-settings",
                        "utilities-tweak-tool"
                    ]
                }
            }
        elif args.section == "places":
            replace_map = {
                "folder-videos": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-videos.svg"
                },
                "folder-pictures": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-pictures.svg"
                },
                "folder-pictures-open": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-pictures-open.svg"
                },
                "folder-music": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-music.svg"
                },
                "folder-music-open": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-music-open.svg"
                },
                "folder-documents": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-documents.svg"
                },
                "folder-download": {
                    "substitute": SUBSTITUTES_PLACES / "kora_folder-download.svg"
                },
                "user-desktop": {
                    "substitute": SUBSTITUTES_PLACES / "kora_user-desktop.svg",
                    # removido pq afeta o ícone de engrenagem, não deve ser mudado
                    #"aliases": [
                    #    "gnome-desktop-config"
                    #]
                },
                "user-home": {
                    "substitute": SUBSTITUTES_PLACES / "kora_user-home.svg"
                }
            }

        repo_destinations = [
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat"),
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat-light"),
            Path("/mnt/seagate/workspace/coding/projects/icons/copycat/copycat-light-panel")
        ]

        local_destinations = [
            Path("/home/luan/.local/share/icons/copycat"),
            #Path("/home/luan/.local/share/icons/copycat-light"),
            #Path("/home/luan/.local/share/icons/copycat-light-panel")
        ]

        if args.replacelevel == "repo":
            # atualizar o repo dos ícones
            destinations = repo_destinations
        elif args.replacelevel == "local":
            # atualizar só localmente
            destinations = local_destinations
        else:
            # atualizar os dois
            destinations = repo_destinations + local_destinations

        # obter os valores do replace_map, obttendo a chave e os valores das entradas
        # então, pra cada 
        for key, entry in replace_map.items():
            # adicionar key na lista de aliases (caso o campo de aliases exista)
            # por que em alguns casos um alias do software pode também ser a key
            aliases = entry.get("aliases", [])
            aliases.append(key)

            replace.replace(
                target_names=aliases,
                substitute_file=entry["substitute"],
                destinations_dirs=destinations
            )
main()