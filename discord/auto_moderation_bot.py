import os
import discord
from libs import macro
from pretty_help import PrettyHelp
from pretty_help import DefaultMenu
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
Prefix = os.getenv('Discord_Prefix')
Token = os.getenv('Discord_Token')
muteRole = "your-mute-roll-name"
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


@bot.command()
async def ban(ctx, member: discord.Member, *,
              reason='Please write a reason!'):
    """
    Ban someone from the server
    """
    if not member:
        return await ctx.send(embed=await macro.error('Provide a member pls?'))

    if not reason:
        return await ctx.send(
            embed=await macro.error(f'Gimme a good reason to ban {member}')
        )

    else:
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(embed=await macro.send(
                desc=f'{member} got ban',
                color=discord.Color.green()))

        except Exception:
            await ctx.send(embed=await macro.send(
                desc=f'Unable to perform the task',
                color=discord.Color.red()))


@bot.command()
async def unban(ctx, name_or_id, *, reason=None):
    """
    Unban someone from the server
    """
    if not name_or_id:
        return await ctx.send(embed=await macro.error('Give me member?'))

    if not reason:
        return await ctx.send(
            embed=await macro.error(
                f'Gimme a good reason to unban {name_or_id}'))

    else:
        ban = await ctx.get_ban(name_or_id)

        try:
            await ctx.guild.unban(ban.user, reason=reason)
            await ctx.send(
                embed=await macro.send(
                    desc=f'Unbanned {name_or_id}',
                    color=discord.Color.green()))
        except Exception:
            await ctx.send(
                embed=await macro.send(
                    desc=f'Unable Unbanned {name_or_id}',
                    color=discord.Color.red()))


@bot.command()
async def kick(ctx, member: discord.Member, *,
               reason='Please write a reason!'):
    """
    Kick someone from the server
    """
    if not member:
        return await ctx.send(embed=await macro.error('Provide member pls?'))

    if not reason:
        return await ctx.send(
            embed=await macro.error(f'Gimme a good reason to kick {member}'))

    else:
        try:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(
                embed=await macro.send(
                    desc=f'Kicked {member}',
                    color=discord.Color.green()))

        except Exception:
            await ctx.send(
                embed=await macro.send(
                    desc=f'Unable to kick {member}',
                    color=discord.Color.green()))


@bot.command()
async def purge(ctx, limit: int):
    """
    Clean messages from chat
    """
    if not limit:
        return await ctx.send(
            embed=await macro.error(
                'Enter the number of messages you want me to delete.'))

    if limit < 99:
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit)
        succ = f'Successfully deleted {len(deleted)} message(s)'
        await ctx.channel.send(
            embed=await macro.send(desc=succ),
            delete_after=6)

    else:
        await ctx.send(
            embed=await macro.error(
                f'Cannot delete `{limit}`, try with less than 100.',
                delete_after=23))


@bot.command()
async def mute(ctx, member: discord.Member, *,
               muteRole: str = None):
    """
    Mute a Member
    """
    if not member and muteRole is None:
        return await ctx.send(
            embed=await macro.error('To whom do I Mute?'))

    if muteRole is not None:
        role = discord.utils.find(
            lambda m: muteRole.lower() in m.name.lower(),
            ctx.message.guild.roles)
        if not role:
            return await ctx.send(
                embed=await macro.error('That role does not exist.'))
        try:
            await member.add_roles(role)
            await ctx.message.delete()
            await ctx.send(
                embed=await macro.send(
                    desc=f'Muted *{member.display_name}*'))
        except Exception:
            await ctx.send(embed=await macro.error("unable to mute member"))

    else:
        return await ctx.send(
            embed=await macro.error('Please mention the member to Mute .'))


@bot.command()
async def unmute(ctx, member: discord.Member, *, muteRole: str):
    """
    Remove mute from member
    """
    role = discord.utils.find(
        lambda m: muteRole.lower() in m.name.lower(),
        ctx.message.guild.roles)
    if not role:
        return await ctx.send(embed=await macro.error(
            'That role does not exist.'))
    try:
        await member.remove_roles(role)
        await ctx.message.delete()
        await ctx.send(
            embed=await macro.error(
                f'Removed: Mute from *{member.display_name}*'))
    except Exception:
        await ctx.send(
            embed=await macro.error(
                "I don't have the perms to remove that role."))


@bot.command()
async def poll(ctx, *, message):
    msg = await ctx.channel.send(embed=await macro.send(
        desc=f"{message}",
        footer="poll by {ctx.author.display_name}"))
    await msg.message.add_reaction('⬆')
    await msg.message.add_reaction('⬇')


@bot.command()
async def bans(ctx):
    """
    See a list of banned users
    """
    try:
        bans = await ctx.guild.bans()
    except Exception:
        return await ctx.send(
            embed=await macro.error(
                "You don't have the perms to see bans. (｡◝‿◜｡)"))
    result = ',\n'.join(
        ["[" + (str(b.user.id) + "] " + str(b.user)) for b in bans])
    if len(result) < 1990:
        total = result
    else:
        total = result[:1990]
    await ctx.send(
        embed=await macro.send(
            desc=f"```bf\n{total}```",
            icon=ctx.guild.icon_url))


@bot.command()
async def baninfo(ctx, *, name_or_id):
    """
    Check the reason of a ban
    """
    ban = await ctx.get_ban(name_or_id)
    e = discord.Embed(color=discord.Color.random())
    e.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
    e.add_field(name='Reason', value=ban.reason or 'None')
    e.set_thumbnail(url=ban.user.avatar_url)
    e.set_footer(text=f'User ID: {ban.user.id}')
    await ctx.send(embed=e)


@bot.command()
async def removerole(ctx, member: discord.Member, *, rolename: str):
    """
    Remove a role from someone
    """
    role = discord.utils.find(
        lambda m: rolename.lower() in m.name.lower(),
        ctx.message.guild.roles)
    if not role:
        return await ctx.send(
            embed=await macro.error('That role does not exist.'))
    try:
        await member.remove_roles(role)
        await ctx.message.delete()
        await ctx.send(
            embed=await macro.send(
                desc=f'Removed: `{role.name}` role from \
                *{member.display_name}*'
            ))
    except Exception:
        await ctx.send(
            embed=await macro.error(
                "I don't have the perms to remove that role."))


@bot.command()
async def addrole(
        ctx,
        member: discord.Member,
        *,
        rolename: str = None):
    """
    Add a role to someone else
    Usage:
    addrole @name Listener
    """
    if not member and rolename is None:
        return await ctx.send(
            embed=await macro.error('To whom do I add which role?'))

    if rolename is not None:
        role = discord.utils.find(
            lambda m: rolename.lower() in m.name.lower(),
            ctx.message.guild.roles)
        if not role:
            return await ctx.send(
                embed=await macro.error('That role does not exist.'))
        try:
            await member.add_roles(role)
            await ctx.message.delete()
            await ctx.send(
                embed=await macro.send(
                    desc=f'Added: **`{role.name}`** \
                    role to *{member.display_name}*'))
        except Exception:
            await ctx.send(
                embed=await macro.send(
                    desc="I don't have the perms to add that role."))

    else:
        return await ctx.send(
            embed=await macro.error(
                'Please mention the member and role to give them.'))


for filename in os.listdir('/cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.filename[:-3]")

bot.run(Token)
