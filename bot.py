import logging
import discord
import constants
from secrets import randbelow

allowed_roles = [discord.Object(id_) for id_ in constants.MODERATION_ROLES]

client = discord.Client


class MoocahBot(client):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

    async def on_ready(self):
        print('ready!')

    async def on_message(self, msg: discord.Message) -> None:
        if msg.author.bot:
            return
        if msg.content == '.m':
            if any(role.id in constants.MODERATION_ROLES for role in msg.author.roles):
                self.active = not self.active
                print(f'toggled to {self.active}')
                return
        elif not self.active:
            return
        else:
            roll = randbelow(1000)
            if not roll:
                await msg.channel.send(f'{msg.author.mention} Cunt.')


bot = MoocahBot(
    activity=discord.Activity(
        type=discord.ActivityType.watching, name='You'),
    max_messages=10000,
    allowed_mentions=discord.AllowedMentions(
        everyone=False, roles=allowed_roles),
    guild_ready_timeout=10.0
)
bot.run(constants.Bot.token)
