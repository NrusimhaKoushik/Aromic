from logging.config import dictConfig

TOKEN='MTA1NTQzNzEwMjA0MjU5OTQ0NQ.G86Kyt.kc9qGpprApa1YPbGN3nfgz6mDfr8hukVtCGsZI'
guild_ids=999541224404942848

API_KEY='AIzaSyA-kPAKirsOa9oc_P6jwlERGrSPvCDqsi8'
CX='35b1cbb421eb7470d'

BOT_ID = '1055437102042599445'

DISCORD_BOT_LIST_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6IjEwNTU0MzcxMDIwNDI1OTk0NDUiLCJpYXQiOjE2OTU5MDQ5Nzh9.IoP3Gtp6fV5sl2gfI7oHn3OJraO08X3fNF9kOCibYqw'

APOD_API = 'YDsaWyDwHRUjtKNZBjo4a86krTdvZaHLvVRcMThW'

IMAGE_ACCESS_KEY='8_4Gt0TJbffpJrMBoHtQy9svbC-BPRBzYdBzzWIcQ_0'

LAVALINK_HOST = 'http://narco.buses.rocks:2269'
LAVALINK_PASSWORD='glasshost1984'

CLIENT_ID = '0a3fec3749544e8e8515ea7611a45ca3'
CLIENT_SECRET = 'c923b950b09f4a18b46410401819d122'

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-5s - %(name)-5s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)