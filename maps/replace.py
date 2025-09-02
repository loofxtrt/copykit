from src.utils.paths import SUBSTITUTES_APPS, SUBSTITUTES_SYSTEM, SUBSTITUTES_PLACES, SUBSTITUTES_MIMETYPES

software = {
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
    "aseprite": {
        "substitute": SUBSTITUTES_APPS / "aseprite.svg",
        "aliases": [
            "lutris_aseprite"
        ]
    },
    "libresprite": {
        "substitute": SUBSTITUTES_APPS / "libresprite.svg",
        "aliases": [
            "com.github.libresprite.LibreSprite"
        ],
        "force_creation_in": "apps/scalable",
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
    "roblox-player": {
        "substitute": SUBSTITUTES_APPS / "roblox-player.svg",
        "aliases": [
            "io.github.vinegarhq.Vinegar.player",
            "net.brinkervii.grapejuice.robloxplayer",
            "grapejuice-roblox-player"
        ],
        "ignore_key": True,        
        "force_creation_in": "apps/scalable/"
    },
    "roblox-studio": {
        "substitute": SUBSTITUTES_APPS / "roblox-studio.svg",
        "aliases": [
            "io.github.vinegarhq.Vinegar.studio",
            "grapejuice-roblox-studio",
            "net.brinkervii.grapejuice.robloxstudio",
            "org.vinegarhq.Vinegar.studio"
        ],
        "ignore_key": True,
        "force_creation_in": "apps/scalable/"
    },
    "sober": {
        "substitute": SUBSTITUTES_APPS / "roblox-sober.svg",
        "aliases": [
            "org.vinegarhq.Sober"
        ],
        "ignore_key": True,
        "force_creation_in": "apps/scalable/"
    },
    "vinegar": {
        "substitute": SUBSTITUTES_APPS / "roblox-vinegar.svg",
        "aliases": [
            "io.github.vinegarhq.Vinegar",
            "org.vinegarhq.Vinegar"
        ],
        "ignore_key": True,
        "force_creation_in": "apps/scalable/"
    },
    "audacity": {
        "substitute": SUBSTITUTES_APPS / "audacity.svg",
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
        "substitute": SUBSTITUTES_APPS / "kora_btop.svg",
        "force_creation_in": "apps/scalable/"
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
            "xarchiver",
            "file-roller.svgi"
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
    },
    "java21-openjdk": {
        "substitute": SUBSTITUTES_APPS / "kora_java.svg",
        "force_creation_in": "apps/scalable/"
    },
    "trenchbroom": {
        "substitute": SUBSTITUTES_APPS / "trenchbroom.svg",
        "aliases": [
            "com.kristianduske.TrenchBroom"
        ],
        "force_creation_in": "apps/scalable/",
        "ignore_key": True
    },
    "minecraft": {
        "substitute": SUBSTITUTES_APPS / "minecraft.svg",
        "aliases": [
            "com.mojang.Minecraft",
            "minecraft-launcher"
        ]
    },
    "librewolf": {
        "substitute": SUBSTITUTES_APPS / "librewolf.svg",
        "aliases": [
            "appimagekit-librewolf",
            "io.gitlab.LibreWolf",
            "io.gitlab.librewolf-community"
        ]
    },
    "animeeffects": {
        "substitute": SUBSTITUTES_APPS / "animeeffects.svg",
        "aliases": [
            "AnimeEffects"
        ],
        "ignore_key": True,
        "force_creation_in": "apps/scalable"
    },
    "mpv": {
        "substitute": SUBSTITUTES_APPS / "breeze-dark_mpv.svg",
        "aliases": [
            "mplayer"
        ]
    },
    "protoncalendar": {
        "substitute": SUBSTITUTES_APPS / "kora_protoncalendar.svg"
    }
}

# system = {
#     "settings": {
#         "substitute": SUBSTITUTES_SYSTEM / "reversal-black_cosmic-settings.svg",
#         "aliases": [
#             "computersettings",
#             "org.xfce.settings.manager",
#             "redhat-system_settings",
#             "com.system76.CosmicSettings",
#             "package-settings",
#             "systemsettings",
#             "gnome-settings",
#             "package_settings",
#             "xfce4-settings",
#             "org.gnome.Settings",
#             "redhat-server_settings",
#             "xfce-system-settings",
#             "utilities-tweak-tool"
#         ]
#     }
# }
system = {
    "settings": {
        "substitute": SUBSTITUTES_SYSTEM / "reversal-black_cosmic-settings.svg",
        "aliases": [
            "preferences-system.svg",
            "utilities-tweak-tool.svg",
            "configuration-section"
        ]
    }
}

places = {
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

mimetypes = {
    "zip": {
        "substitute": SUBSTITUTES_MIMETYPES / "kora_zip-2.svg",
        "aliases": [
            "7zip",
            "application-7zip",
            "application-archive-blank",
            "application-archive",
            "application-archive-zip",
            "application-gzip",
            "application-vnd.kde.fontspackage",
            "application-vnd.kde.okular-archive",
            "application-vnd.ms-cab-compressed",
            "application-vnd.rar",
            "application-x-7z-ace",
            "application-x-7z-arj",
            "application-x-7z-compressed",
            "application-x-7zip",
            "application-x-ace",
            "application-x-archive",
            "application-x-arc",
            "application-x-arj",
            "application-x-ar",
            "application-x-awk",
            "application-x-bzdvi",
            "application-x-bzip-compressed",
            "application-x-bzip-compressed-tar",
            "application-x-bzip",
            "application-x-compressed-iso",
            "application-x-compressed",
            "application-x-compressed-tar",
            "application-x-compress",
            "application-x-compress-tar",
            "application-x-cpio",
            "application-x-gzdvi",
            "application-x-gz-font-linux-psf",
            "application-x-gzip",
            "application-x-kns",
            "application-x-lha",
            "application-x-lhz",
            "application-x-lz4-compressed-tar",
            "application-x-lzip-compressed-tar",
            "application-x-lzma-compressed-tar",
            "application-x-lzma",
            "application-x-lzop",
            "application-x-rar",
            "application-x-shar",
            "application-x-stuffit",
            "application-x-superkaramba",
            "application-x-tar",
            "application-x-tarz",
            "application-x-texgzdvi",
            "application-x-tex-pk",
            "application-x-tha",
            "application-x-thz",
            "application-x-tzo",
            "application-x-xz-compressed-tar",
            "application-x-xz",
            "application-x-zip",
            "application-x-zoo",
            "application-zip",
            "archive",
            "folder-tar",
            "folder_tar",
            "gnome-mime-application-vnd.ms-cab-compressed",
            "gnome-mime-application-x-7z-compressed",
            "gnome-mime-application-x-7zip",
            "gnome-mime-application-x-ace",
            "gnome-mime-application-x-archive",
            "gnome-mime-application-x-arj",
            "gnome-mime-application-x-bzip-compressed",
            "gnome-mime-application-x-bzip-compressed-tar",
            "gnome-mime-application-x-bzip",
            "gnome-mime-application-x-compressed-tar",
            "gnome-mime-application-x-compress",
            "gnome-mime-application-x-cpio-compressed",
            "gnome-mime-application-x-cpio-compress",
            "gnome-mime-application-x-cpio",
            "gnome-mime-application-x-gzip",
            "gnome-mime-application-x-lha",
            "gnome-mime-application-x-lhz",
            "gnome-mime-application-x-lzma-compressed-tar",
            "gnome-mime-application-x-lzma",
            "gnome-mime-application-x-lzop",
            "gnome-mime-application-x-rar",
            "gnome-mime-application-x-shar",
            "gnome-mime-application-x-stuffit",
            "gnome-mime-application-x-tar",
            "gnome-mime-application-x-tarz",
            "gnome-mime-application-x-zip",
            "gnome-mime-application-x-zoo",
            "gnome-mime-application-zip",
            "rar",
            "tar",
            "tgz",
            "viewdvi"
        ],
        "delete_aliases_make_symlinks": [True, "mimetypes/scalable"]
    }
}