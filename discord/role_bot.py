"""
Not tested
"""

import os
import discord
from libs import macro
from pretty_help import PrettyHelp
from pretty_help import DefaultMenu
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv('Disocrd_Token')
Prefix = os.getenv('Disocrd_Prefix')
# your channel id
channel_ID = 1021231231231
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(Prefix),
                   intents=intents,
                   help_command=PrettyHelp())

help_menu = DefaultMenu(active_time=5, remove="⛔")
bot.help_command = PrettyHelp(menu=help_menu)


@bot.event
async def on_ready():
    print(bot.user)
    print("is now alive")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="a movie"
        )
    )

# Make Role
# Delete Role
# Reaction Role


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


@bot.event
async def on_message(message):
    Channel = client.get_channel(channel_ID)
    Moji = await Channel.send(await macro.send(desc=f'{message}', title=f'react role by {message.author.name}'))
    await Moji.add_reaction('🏃')

@bot.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(channel_ID)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "🏃":
      Role = discord.utils.get(user.server.roles, name="yor-role-name-here")
      await user.add_roles(Role)


@bot.command(aliases=['load'])
async def load_cog(ctx, extention):
    """
    Extention Load Command
    """
    bot.load_extension(f'cogs.{extention}')
    await ctx.send(embed=await macro.send(desc=f"loaded {extention}"))


@bot.command(aliases=['unload'])
async def unload_cog(ctx, extention):
    """
    Extention Unload Command
    """
    bot.unload_extension(f'cogs.{extention}')
    await ctx.send(embed=await macro.send(desc=f"unloaded {extention}"))


@bot.command(aliases=['reload'])
async def reload_cog(ctx, extention):
    """
    Extention Reaload Command
    """
    bot.unload_extension(f'cogs.{extention}')
    bot.load_extension(f'cogs.{extention}')
    await ctx.send(embed=await macro.send(desc=f"reloaded {extention}"))

bot.run(Token)
