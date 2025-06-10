import discord
from functools import wraps
from discord.ext import commands
from typing import Union

from src import NayulCore
from .others import format_timestamp

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

def check_user_banned():
    """Verifica se o usuário está banido do bot."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, inter: Union[discord.Interaction, discord.Message], *args, **kwargs):
            if isinstance(inter, discord.Interaction):
                user = inter.user
                nayul: NayulCore = inter.client
            else:
                user = inter.author
                nayul: NayulCore = self.nayul
            
            user_data = await nayul.db.users.get_user(user)

            if user_data.ban.banned:
                if isinstance(inter, discord.Interaction):
                    banned_at = user_data.ban.banned_at
                    expires_at = user_data.ban.expires_at

                    if expires_at:
                        expires_str = f'{format_timestamp(expires_at, "F")} ({format_timestamp(expires_at, "R")})'
                    else:
                        expires_str = 'Nunca (Permanente)'

                    message = (
                        f'⚠️{inter.user.mention} está **banido de usar todas as funcionalidades** da {self.nayul.user.name}.\n'
                        f'**Banido em:** {format_timestamp(banned_at, "F")} ({format_timestamp(banned_at, "R")})\n'
                        f'**Expira em:** {expires_str}\n'
                        f'**Motivo:** {user_data.ban.reason}\n'
                        '-# Se você acredita que isso é um erro, entre em contato com a equipe do bot.'
                    )
                    await inter.response.send_message(
                        content=message,
                        ephemeral=True,
                        allowed_mentions=discord.AllowedMentions.none()
                    )
                return

            return await func(self, inter, *args, **kwargs)
        return wrapper
    return decorator