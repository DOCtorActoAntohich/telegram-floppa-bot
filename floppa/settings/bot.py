from pydantic import BaseSettings, Field


class _BotSettings(BaseSettings):
    token: str = Field(..., env="BOT_TOKEN")
    alias: str = Field(..., env="BOT_ALIAS")
    creator_ids: list[int] = Field(..., env="BOT_CREATOR_IDS")
