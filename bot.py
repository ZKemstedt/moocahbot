from pathlib import Path
import yaml
import discord
import constants
from secrets import randbelow

allowed_roles = [discord.Object(id_) for id_ in constants.MODERATION_ROLES]
filename = 'stats.yml'


class MoocahBot(discord.Client):
    """A simplistic bot that has a 0.01% change of responding to any message with 'cunt.'"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

        # load stats from statfile
        # Check if the file exists, create if it not
        file = Path(filename)
        if not file.exists():
            print(f"Creating {filename}")
            file.touch()
            self.data = []
        else:
            # load data
            with open(filename, encoding="UTF-8") as f:
                self.data = yaml.safe_load(f)

    async def close(self):
        """Overrides the client.close() method to also save stats."""
        # sava data
        with open(filename, 'w', encoding="UTF-8") as f:
            yaml.dump(self.data, f)
        await super().close()

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
                return
        elif msg.content == '.mstats':
            await msg.channel.send(f'{len(self.data)} cunts have been told off.')
            return
        elif not self.active:
            return
        roll = randbelow(1000)
        if not roll:
            self.data.append(msg.author.id)
            await msg.channel.send(f'{msg.author.mention} Cunt.')


bot = MoocahBot(
    activity=discord.Activity(type=discord.ActivityType.watching, name='You'),
    max_messages=10000,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=allowed_roles),
    guild_ready_timeout=10.0
)
bot.run(constants.Bot.token)
