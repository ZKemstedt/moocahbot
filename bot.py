import discord
import constants
from secrets import randbelow

allowed_roles = [discord.Object(id_) for id_ in constants.MODERATION_ROLES]

client = discord.Client


class MoocahBot(client):
    """A simplistic bot that has a 0.01% change of responding to any message with 'cunt.'"""

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
                if not self.active:
                    emote = constants.Style.Emojis.status_offline
                else:
                    emote = constants.Style.Emojis.status_online
                await msg.channel.send(f'Toggled to {emote}')
                # print(f'toggled to {emote}')
                return
        elif not self.active:
            return

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
