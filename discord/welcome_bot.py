import os
import random
import discord

from discord import File
from discord.utils import get
from discord.ext import commands

from easy_pil import load_image_async
from easy_pil import Editor
from easy_pil import Font
from dotenv import load_dotenv

from libs import macro

load_dotenv()

intents = discord.Intents.default()
intents.members = True

Dis_Url = "https://discord.com/channels/947089950984261662/947089950984261665"

Token = os.getenv('Disocrd_Token')
Prefix = os.getenv('Disocrd_Prefix')
ChannelID = 953517114801659924

# file management
files = ['Breeze.png', 'Candy.png', 'Crimson.png', 'Falcon.png',
         'Meadow.png', 'Midnight.png', 'Raindrop.png', 'Sunset.png']

# font management
poppins = Font.poppins(size=50, variant="bold")
poppins_small = Font.poppins(size=35, variant="light")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(Prefix),
    intents=intents)


@bot.event
async def on_command_error(ctx, error):
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
async def on_ready():
    print("Bot now online")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="I D K"))


@bot.event
async def on_member_join(member):
    image_name = random.choice(files)

    # add the channel id in which you want to send the card
    channel = bot.get_channel(ChannelID)

    # if you want to give any specific roles
    # to any user then you can add like this
    role = get(member.guild.roles, name="Member")
    await member.add_roles(role)

    # Counting the postion of the new member
    j = member.joined_at
    g = member.guild.members
    pos = sum(m.joined_at < j for m in g if m.joined_at is not None)

    if pos == 1:
        te = "st"
    elif pos == 2:
        te = "nd"
    elif pos == 3:
        te = "rd"
    else:
        te = "th"

    background = Editor("./images/" + image_name)
    profile_image = await load_image_async(str(member.avatar.url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()

    background.paste(profile, (70, 130))
    # background.ellipse((325, 90), 150, 150, outline="gold", stroke_width=4)

    # drop shadow

    background.text(
        (614, 141),
        f"WELCOME TO",
        color="#000000",
        font=poppins,
        align="center"
    )

    background.text(
        (614, 190),
        f"{member.guild.name}",
        color="#000000",
        font=poppins,
        align="center"
    )

    background.text(
        (613, 140),
        f"WELCOME TO",
        color="white",
        font=poppins,
        align="center"
    )

    background.text(
        (613, 190),
        f"{member.guild.name}",
        color="white",
        font=poppins,
        align="center"
    )

    # drop shadow

    background.text((614, 261), f"{member.name}#{member.discriminator}",
                    color="#000000", font=poppins_small, align="center")
    background.text((614, 301), f"You Are The {pos}{te} Member",
                    color="#000000", font=poppins_small, align="center")

    background.text((613, 260), f"{member.name}#{member.discriminator}",
                    color="#FFFAFA", font=poppins_small, align="center")
    background.text((613, 300), f"You Are The {pos}{te} Member",
                    color="#FFFAFA", font=poppins_small, align="center")

    file = File(fp=background.image_bytes, filename="wlcbg.jpg")

    # if you want to message more message then you can add like this
    await channel.send(
        f"Heya {member.mention}! \
        Welcome To **{member.guild.name} \
        For More Information Go To <#951767335830712360>**"
    )

    # for sending the card
    await channel.send(file=file)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(ChannelID)

    await channel.send(
        f"{member.name} Has Left The server, We are going to miss you :( "
    )


@bot.command(aliases=['load'])
async def load_cog(ctx, extention):
    bot.load_extension(f'cogs.{extention}')


@bot.command(aliases=['unload'])
async def unload_cog(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')


@bot.command(aliases=['reload'])
async def reload_cog(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')
    bot.load_extension(f'cogs.{extention}')

for filename in os.listdir('/cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.filename[:-3]")

bot.run(Token)
