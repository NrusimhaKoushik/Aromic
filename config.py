from logging.config import dictConfig

TOKEN='DISCORD_TOKEN'

API_KEY='YOUR_GOOGLE_API_KEY'
CX='YOUR_GOOGLE_CX'

BOT_ID = 'BOT_ID'

DISCORD_BOT_LIST_TOKEN = 'BOT_DBL_TOKEN'

APOD_API = 'YOUR_APOD_API'

IMAGE_ACCESS_KEY='YOUR_IMAGE_KEY'

LAVALINK_HOST = 'YOUR_LAVALINK_HOST'
LAVALINK_PASSWORD='YOUR_LAVALINK_PASSWORD'

CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

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
