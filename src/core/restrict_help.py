import discord
from discord.ext import commands
from discord.ext.commands import HelpCommand, Group, Command
from typing import Mapping, Optional

class RestrictedHelpCommand(HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'help': 'Mostra este menu de ajuda.'})

    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], list[Command]]):
        if not await self.is_authorized(self.context.author.id):
            return

        embed = discord.Embed(
            title='📖 Lista de Comandos',
            color=discord.Color.blurple()
        )

        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            if not filtered:
                continue

            value_lines = []
            for command in filtered:
                if isinstance(command, Group):
                    subcommands = await self.filter_commands(command.commands, sort=True)
                    if subcommands:
                        sub_list = '\n'.join(
                            f'  ↳ `{self.context.prefix}{command.name} {sub.name}` - {sub.description or "Sem descrição"}'
                            for sub in subcommands
                        )
                        value_lines.append(
                            f'`{self.context.prefix}{command.name}` - {command.description or "Sem descrição"}\n{sub_list}\n\n'
                        )
                    else:
                        value_lines.append(f'`{self.context.prefix}{command.name}` - {command.description or "Sem descrição"}\n')
                else:
                    value_lines.append(f'`{self.context.prefix}{command.name}` - {command.description or "Sem descrição"}\n')

            cog_name = cog.qualified_name if cog else 'Sem categoria'
            embed.add_field(name=cog_name, value=''.join(value_lines), inline=False)

        await self.get_destination().send(embed=embed, delete_after=20)

    async def is_authorized(self, user_id: int) -> bool:
        settings = await self.context.bot.db.settings.get_settings()
        return user_id in settings.staffs or user_id in self.context.bot.owner_ids