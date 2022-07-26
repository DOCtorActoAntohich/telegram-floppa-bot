from floppa.settings.bot import _BotSettings
from floppa.settings.mongo import _MongoSettings


class Settings:
    bot = _BotSettings()
    mongo = _MongoSettings()
