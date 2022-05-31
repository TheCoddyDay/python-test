import discord
from discord.ext import commands


class Example(commands.Cog):
    """
    an example cog bot
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ok')

    @commands.command()
    async def name(self, ctx):
        await ctx.send(f"{ctx.author.display_name}")


def setup(bot):
    bot.add_cogs(Example(bot))
