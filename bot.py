import discord
import constants
from secrets import randbelow

allowed_roles = [discord.Object(id_) for id_ in constants.MODERATION_ROLES]
bot = discord.Client(
    activity=discord.Activity(
        type=discord.ActivityType.watching, name='You'),
    max_messages=10000,
    allowed_mentions=discord.AllowedMentions(
        everyone=False, roles=allowed_roles),
    guild_ready_timeout=10.0
)


class MoocahBot(discord.client):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

    async def on_message(self, msg: discord.Message) -> None:
        if msg.author.bot:
            return
        elif not self.active:
            return
        elif (any(role in constants.MODERATION_ROLES for role in msg.author.roles)
              and msg.content == '.m'):
            self.active = not self.active
        else:
            roll = randbelow(10)
            if not roll:
                await msg.channel.send(f'{msg.author.mention} Cunt.')


bot.run(constants.Bot.token)
