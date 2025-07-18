import discord
from discord.ext import commands

from src import NayulCore

class OwnerCommands(commands.Cog):
    def __init__(self, nayul: NayulCore):
        self.nayul = nayul

    @commands.command(name='sync', description='Sincroniza os comandos.')
    @commands.is_owner()
    async def sync(self, ctx: commands.Context[NayulCore]):
        """Sincroniza os comandos da Nayul com o Discord."""
        try:
            cmd = await self.nayul.tree.sync()
            await ctx.reply(f'Comandos sincronizados com sucesso. ({len(cmd)})', delete_after=60, mention_author=False)
        except Exception as e:
            await ctx.reply(f'Erro ao sincronizar os comandos: {e}', delete_after=60, mention_author=False)

    #-------------------- Staff Manager --------------------#

    @commands.group(name='staff')
    @commands.is_owner()
    async def staff(self, ctx: commands.Context[NayulCore]):
        """Gerencia os staffs da Nayul."""
        if not ctx.invoked_subcommand:
            await ctx.reply('Use um subcomando: add, remove ou list.', delete_after=60, mention_author=False)

    @staff.command(name='add', description='Adiciona um staff.')
    @commands.is_owner()
    async def add(self, ctx: commands.Context[NayulCore], user: discord.User):
        """Adiciona um staff à Nayul."""
        await self.nayul.db.settings.update_staffs('add', user.id)
        await ctx.reply(f'{user.mention} foi adicionado como staff.', delete_after=60, mention_author=False)

    @staff.command(name='remove', description='Remove um staff.')
    @commands.is_owner()
    async def remove(self, ctx: commands.Context[NayulCore], user: discord.User):
        """Remove um staff da Nayul."""
        await self.nayul.db.settings.update_staffs('remove', user.id)
        await ctx.reply(f'{user.mention} foi removido como staff.', delete_after=60, mention_author=False)
    
    @staff.command(name='list', description='Lista os staffs.')
    @commands.is_owner()
    async def list(self, ctx: commands.Context[NayulCore]):
        """Lista os staffs da Nayul."""
        settings = await self.nayul.db.settings.get_settings()
        staffs = []
        for staff in settings.staffs + list(self.nayul.owner_ids):
            user = await self.nayul.fetch_user(staff)
            staffs.append(f'{user.name} - {user.id}')
        await ctx.reply('\n'.join(staffs) or 'Nenhum staff encontrado.', delete_after=120, mention_author=False)

    #-------------------- Cog Manager --------------------#
        
    @commands.group(name='cog')
    @commands.is_owner()
    async def cogs(self, ctx: commands.Context[NayulCore]):
        """Gerencia as extensões da Nayul."""
        if not ctx.invoked_subcommand:
            await ctx.reply('Use um subcomando: reload, load, unload ou list.', delete_after=60, mention_author=False)

    @cogs.command(name='reload', description='Recarrega uma extensão.')
    @commands.is_owner()
    async def reload(self, ctx: commands.Context[NayulCore], extension: str):
        """Recarrega uma extensão ou todas as extensões da Nayul."""
        if extension == 'all':
            await self.nayul.cog_manager.reload_cogs(self.nayul)
            await ctx.reply('Todas as extensões foram recarregadas com sucesso.', delete_after=60, mention_author=False)
            return
        elif extension not in self.nayul.cog_manager.extensions:
            await ctx.reply(f'Extensão `{extension}` não encontrada. Use `{ctx.prefix}cog list` para verificar as extensões`', delete_after=10, mention_author=False)
            return
        
        await self.nayul.cog_manager.reload_cog_one(self.nayul, extension)
        await ctx.reply(f'Extensão `{extension}` recarregada com sucesso.', delete_after=60, mention_author=False)

    @cogs.command(name='load', description='Carrega uma extensão.')
    @commands.is_owner()
    async def load(self, ctx: commands.Context[NayulCore], extension: str):
        """Carrega uma extensão ou todas as extensões da Nayul."""
        if extension == 'all':
            await self.nayul.cog_manager.load_cogs(self.nayul)
            await ctx.reply('Todas as extensões foram carregadas com sucesso.', delete_after=60, mention_author=False)
        elif extension not in self.nayul.cog_manager.extensions:
            await ctx.reply(f'Extensão `{extension}` não encontrada. Use `{ctx.prefix}cog list` para verificar as extensões`', delete_after=10, mention_author=False)
            return
        
        await self.nayul.cog_manager.load_cog_one(self.nayul, extension)
        await ctx.reply(f'Extensão `{extension}` carregada com sucesso.', delete_after=60, mention_author=False)

    @cogs.command(name='unload', description='Descarrega uma extensão.')
    @commands.is_owner()
    async def unload(self, ctx: commands.Context[NayulCore], extension: str):
        """Descarrega uma extensão ou todas as extensões da Nayul."""
        if extension == 'all':
            await self.nayul.cog_manager.unload_cogs(self.nayul)
            await ctx.reply('Todas as extensões foram descarregadas com sucesso.', delete_after=60, mention_author=False)
            return
        elif extension not in self.nayul.cog_manager.extensions:
            await ctx.reply(f'Extensão `{extension}` não encontrada. Use `{ctx.prefix}cog list` para verificar as extensões`', delete_after=10, mention_author=False)
            return
        
        await self.nayul.cog_manager.unload_cog_one(self.nayul, extension)
        await ctx.reply(f'Extensão `{extension}` descarregada com sucesso.', delete_after=60, mention_author=False)

    @cogs.command(name='list', description='Lista todas as extensões.')
    @commands.is_owner()
    async def extensions(self, ctx: commands.Context[NayulCore]):
        """Lista todas as extensões da Nayul."""
        extensions = self.nayul.cog_manager.extensions.keys()
        extensions_str = ' - all (Aplica em todas as extensões)\n - ' + '\n - '.join(list(extensions))
        await ctx.reply(f'Extensões:```\n{extensions_str}```', delete_after=120, mention_author=False)

async def setup(nayul: NayulCore):
    await nayul.add_cog(OwnerCommands(nayul))