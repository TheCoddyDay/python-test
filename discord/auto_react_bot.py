import os
import discord
import asyncio
from libs import macro
from pretty_help import PrettyHelp
from pretty_help import DefaultMenu
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
Prefix = os.getenv('Disocrd_Prefix')
Token = os.getenv('Disocrd_Token')
bot = commands.Bot(command_prefix=commands.when_mentioned_or(Prefix),
                   intents=intents,
                   help_command=PrettyHelp())

help_menu = DefaultMenu(active_time=5, remove="⛔")
bot.help_command = PrettyHelp(menu=help_menu)


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
        name="YOUR NAME"))


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


@bot.event
async def on_message(message):
    if 'hi' == message.content.lower():
        await message.add_reaction("👋🏻")

    elif 'bye' == message.content.lower():
        await message.add_reaction("🤙🏻")

    elif 'hello' == message.content.lower():
        await message.add_reaction("👋🏻")

    elif 'lol' == message.content.lower():
        await message.add_reaction("🤣")

    elif 'hola' == message.content.lower():
        await message.add_reaction("👋🏻")

    elif 'aloha' == message.content.lower():
        await message.add_reaction("👋🏻")

    elif 'hell' == message.content.lower():
        await message.add_reaction("☠")

    elif 'toxic' == message.content.lower():
        await message.add_reaction("☠")

    elif 'not good' == message.content.lower():
        await message.add_reaction("😡")

    elif 'good' == message.content.lower():
        await message.add_reaction("🥰")

    elif 'bruh' == message.content.lower():
        await message.add_reaction("😂")

    elif 'kill' == message.content.lower():
        await message.add_reaction("🔪")

    elif 'live' == message.content.lower():
        await message.add_reaction("🔴")

    elif 'love' == message.content.lower():
        await message.add_reaction("🖤")

    elif 'war' == message.content.lower():
        await message.add_reaction("🔫")

    elif 'fight' == message.content.lower():
        await message.add_reaction("🤬")

    elif 'joke' == message.content.lower():
        await message.add_reaction("😅")

    elif 'nice' == message.content.lower():
        await message.add_reaction("😅")

    elif 'noice' == message.content.lower():
        await message.add_reaction("😎")

    elif 'yes' == message.content.lower():
        await message.add_reaction("✔")

    elif 'no' == message.content.lower():
        await message.add_reaction("❌")

    elif 'break' == message.content.lower():
        await message.add_reaction("💔")

    elif 'up' == message.content.lower():
        await message.add_reaction("⬆")

    elif 'down' == message.content.lower():
        await message.add_reaction("⬇")

    elif 'right' == message.content.lower():
        await message.add_reaction("➡")

    elif 'left' == message.content.lower():
        await message.add_reaction("⬅")

    elif 'happy' == message.content.lower():
        await message.add_reaction("😁")

    elif 'sad' == message.content.lower():
        await message.add_reaction("😢")

    elif 'cry' == message.content.lower():
        await message.add_reaction("😭")

    elif 'angry' == message.content.lower():
        await message.add_reaction("😈")

    elif 'help' == message.content.lower():
        await message.add_reaction("🆘")

    elif 'kind' == message.content.lower():
        await message.add_reaction("👑")

    elif 'strong' == message.content.lower():
        await message.add_reaction("💪🏻")

    elif 'weak' == message.content.lower():
        await message.add_reaction("🧐")

    elif 'when?' == message.content.lower():
        await message.add_reaction("⁉")

    elif 'how?' == message.content.lower():
        await message.add_reaction("⁉")

    elif 'what?' == message.content.lower():
        await message.add_reaction("⁉")

    elif 'why?' == message.content.lower():
        await message.add_reaction("⁉")

    elif 'he' == message.content.lower():
        await message.add_reaction("👦🏻")

    elif 'she' == message.content.lower():
        await message.add_reaction("👧🏻")

    elif 'i' == message.content.lower():
        await message.add_reaction("😑")

    elif 'you' == message.content.lower():
        await message.add_reaction("😑")

    elif 'we' == message.content.lower():
        await message.add_reaction("😑")

    elif 'this' == message.content.lower():
        await message.add_reaction("😶")

    elif 'bad' == message.content.lower():
        await message.add_reaction("🙄")

    elif 'sus' == message.content.lower():
        await message.add_reaction("😨")

    elif 'amoung us' == message.content.lower():
        await message.add_reaction("😱")

    elif 'kinda' == message.content.lower():
        await message.add_reaction("😏")

    elif 'oh' == message.content.lower():
        await message.add_reaction("😮")

    elif 'night' == message.content.lower():
        await message.add_reaction("🌙")

    elif 'midnight' == message.content.lower():
        await message.add_reaction("🕛")

    elif 'day' == message.content.lower():
        await message.add_reaction("🌞")

    elif 'noon' == message.content.lower():
        await message.add_reaction("🕛")

    elif 'hate' == message.content.lower():
        await message.add_reaction("🧨")

    elif 'dizzy' == message.content.lower():
        await message.add_reaction("😵")
        await asyncio.sleep(.4)
        await message.add_reaction("🥴")

    elif 'bored' == message.content.lower():
        await message.add_reaction("🥱")

    elif 'cya' == message.content.lower():
        await message.add_reaction("🙋🏻‍♀️")

    elif 'cu' == message.content.lower():
        await message.add_reaction("🙋🏻‍♂️")

    elif 'ok' == message.content.lower():
        await message.add_reaction("🆗")

    elif 'yeah' == message.content.lower():
        await message.add_reaction("🙂")

    elif 'nope' == message.content.lower():
        await message.add_reaction("🤔")


bot.run(Token)
