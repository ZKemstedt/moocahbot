from pathlib import Path
import yaml
import discord
import constants
from secrets import randbelow
from discord.errors import NotFound, HTTPException

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

        elif msg.content == '.mrank':
            cunts = get_biggest_cunts(self.data)
            str_cunts = {}
            for _id, count in cunts.items():
                user = self.get_user(_id)
                if user is None:
                    try:
                        username = await self.fetch_user(_id)
                        username = username.display_name
                    except NotFound:
                        username = f'{_id}'
                    except HTTPException as e:
                        username = f'{_id}'
                else:
                    username = user.display_name
                str_cunts[username] = count
            await msg.channel.send('\n'.join([f'{name}: {count}' for name, count in str_cunts.items()]))

        elif not self.active:
            return

        roll = randbelow(1000)
        if not roll:
            self.data.append(msg.author.id)
            await msg.channel.send(f'{msg.author.mention} Cunt.')


def get_biggest_cunts(stats) -> str:
    # biggest cunts
    cunt_list = {}
    for cunt in stats:
        if not isinstance(cunt, int):
            continue
        if cunt in cunt_list:
            cunt_list[cunt] += 1
        else:
            cunt_list[cunt] = 1
            
    sorted_cunts = {k: v for k, v in sorted(cunt_list.items(), key=lambda item: item[1])}
    
    return sorted_cunts

# - Leineth | A z r e e
# - Leineth | A z r e e
# - Schulky
# - Leineth | A z r e e
# - Glyphe
# - Schulky
# - Leineth | A z r e e
# - Moocah | Melon
# - Uchaguzi | Ucha


bot = MoocahBot(
    activity=discord.Activity(type=discord.ActivityType.watching, name='You'),
    max_messages=10000,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=allowed_roles),
    guild_ready_timeout=10.0
)
bot.run(constants.Bot.token)
