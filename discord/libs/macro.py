import discord
import datetime


class Macro:
    """
    the BEST macro class :D Its works. you can send embeds in one line of code
    by using this macro calss, just to be simple
    """

    @staticmethod
    async def msg(desc,
                  title=None,
                  color: discord.Color = discord.Color.random(),
                  thumb: str = None,
                  fields: dict = None, footer: str = None,
                  icon: str = None):
        """
        :params:
            desc: Description for embed you have to give it
            title: an optional but Title of thr embed
            color: Color of embed by default its random
            thumb: A thumbnail re-presenter of embed, its also optional
            filed: you can use it as key:str and value:list with inline:str
        :return: discord.Embed()
        """

        if title is None:
            title = "title"

        embed = discord.Embed(
            type='rich',
            description=desc,
            title=title,
            color=color,
            timestamp=datetime.datetime.utcnow()
        )

        if not thumb:
            return embed
        embed.set_thumbnail(url=thumb)

        if not fields:
            return embed

        for field, value in fields.items():
            if isinstance(value, list):
                for i in value:
                    embed.add_field(name=f"{field}",
                                    value=f"{value}",
                                    inline=f"{i}")
            embed.add_field(name=f"{field}", value=f"{value}")

        if not footer:
            return embed

        if not icon:
            return embed

        embed.set_footer(text=footer, icon_url=icon)
        return embed

    @classmethod
    async def img(cls, image: str, desc: str = None, title: str = None):
        """
        A simple class method that helps you to work with images and embeds
        """
        message = await cls.msg(desc=desc, title=title)
        message.set_image(url=image)
        return message

    @classmethod
    async def error(cls,
                    desc: object = None,
                    title: object = None,
                    footer: str = None,
                    icon: str = None) -> object:
        """
        :rtype: object
        """
        return await cls.msg(desc=desc, title=title,
                             color=discord.Color.red())


err, error = Macro.error, Macro.error
send, msg = Macro.msg, Macro.msg
img, pic = Macro.img, Macro.img
