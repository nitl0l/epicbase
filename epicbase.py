import asyncio
import locale
import logging
from datetime import datetime
from os import getenv

from discord import (
    ApplicationContext,
    AutoShardedBot,
    Intents,
    Member,
    User,
)
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv(".env")

logging.basicConfig(level=logging.INFO, format=logging.BASIC_FORMAT)
locale.setlocale(locale.LC_ALL, "")


class Epicbase(AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        asyncio.run(self.on_startup())

    async def on_startup(self):
        self.database = await Tortoise.init(
            db_url="sqlite://epicbase.db", modules={"models": ["cogs.models"]}
        )
        await Tortoise.generate_schemas(safe=True)

    async def on_application_command_completion(self, ctx: ApplicationContext):
        user_data = {}
        if isinstance((user := ctx.user), Member):
            user_data = user._user._to_minimal_user_json()
        elif isinstance(user, User):
            user_data = user._to_minimal_user_json()
        logging.getLogger("Epicbase.client").info(
            "Command received: %s",
            {
                "command": str(ctx.command.qualified_name),
                "time": datetime.now().isoformat(sep=" ", timespec="minutes"),
                "user": user_data,
            },
        )

    async def on_ready(self):
        self.load_extensions("cogs", package="", recursive=True)
        await self.sync_commands(method="auto")


instance = Epicbase(command_prefix="/", intents=Intents.default())
instance.run(getenv("DISCORD_TOKEN"))
