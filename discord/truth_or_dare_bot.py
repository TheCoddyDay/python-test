import os
import discord
import random
import asyncio
from libs import macro
from pretty_help import PrettyHelp
from pretty_help import DefaultMenu
from discord.commands import Option
from discord.commands import SlashCommandGroup
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
Prefix = os.getenv('Discord_Prefix')
Token = os.getenv('Discord_Token')
bot = commands.Bot(command_prefix=commands.when_mentioned_or(Prefix),
                   intents=intents,
                   help_command=PrettyHelp())

help_menu = DefaultMenu(active_time=5, remove="⛔")
bot.help_command = PrettyHelp(menu=help_menu)


def cleanList(ok: list):
    temp = []
    for i in ok:
        temp.append(i.strip())
    return temp


@bot.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))


@bot.event
async def on_ready():
    """
    On Ready Function
    """
    print(bot.user)
    print("-" * 15, "\n is ready")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="Your Truths"))


@bot.event
async def on_command_error(ctx, error):
    """
    Handling Error
    """
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.CommandNotFound)

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=await macro.error(str(error)))

    elif isinstance(error, AssertionError):
        await ctx.send(embed=await macro.error(
            f"{str(error).replace('AssertionError: ', '')}")
        )

    elif isinstance(error, IndexError):
        await ctx.send(embed=await macro.error("Index error"))

    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=await macro.error(
            f"You forgot an argument!\n```{error}```"))
    else:
        await ctx.send(embed=await macro.error(f'Woah there partner. :cowboy: \
            It seems as though you ran into a serious error. \
            \nPlease contact @TheCoddyDay#5100 and DM him the text below, \
            along with the command you used, and \
            how you typed it out.\n```{str(error)}```'))



@bot.command(aliases=['load'])
async def load_cog(ctx, extension):
    """
    Extension Load Command
    """
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(embed=await macro.send(desc=f"loaded {extension}"))


@bot.command(aliases=['unload'])
async def unload_cog(ctx, extension):
    """
    Extension Unload Command
    """
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(embed=await macro.send(desc=f"unloaded {extension}"))


@bot.command(aliases=['reload'])
async def reload_cog(ctx, extension):
    """
    Extension Reload Command
    """
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(embed=await macro.send(desc=f"reloaded {extension}"))

bot.run(Token)
