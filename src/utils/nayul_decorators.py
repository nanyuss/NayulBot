from functools import wraps
from discord.ext import commands

from src import NayulCore

def is_staff():
    """Verifica se o usuário é um staff do bot."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: commands.Context[NayulCore], *args, **kwargs):
            settings = await ctx.bot.db.settings.get_settings()
            if ctx.author.id in settings.staffs or ctx.author.id in ctx.bot.owner_ids:
                return await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator