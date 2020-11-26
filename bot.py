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

        elif msg.content == '.mstats':
            await msg.channel.send(f'{len(self.data)} cunts have been told off.')

        elif msg.content == '.mrank':
            cunt_data = get_biggest_cunts(self.data)
            cunt_names = await self.get_cunt_names(cunt_data)
            sorted_cunts = dict(sorted(cunt_names.items(), key=lambda item: item[1], reverse=True))
            cunt_str = '\n'.join([f'**({f"{i+1}".rjust(2, "0")})**: ({c[1]}) {c[0]}' for i, c in enumerate(sorted_cunts.items())])
            await msg.channel.send(cunt_str)

        elif self.active:
            roll = randbelow(1000)
            if not roll:
                self.data.append(msg.author.id)
                await msg.channel.send(f'{msg.author.mention} Cunt.')
    
    async def get_cunt_names(self, cunts):
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
        return str_cunts



def get_biggest_cunts(stats) -> str:
    # biggest cunts
    cunt_list = {}
    for cunt in stats:
        if cunt in cunt_list:
            cunt_list[cunt] += 1
        else:
            cunt_list[cunt] = 1
    return cunt_list
            
    # sorted_cunts = {k: v for k, v in sorted(cunt_list.items(), key=lambda item: item[1])}
    
    # return sorted_cunts


bot = MoocahBot(
    activity=discord.Activity(type=discord.ActivityType.watching, name='You'),
    max_messages=10000,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=allowed_roles),
    guild_ready_timeout=10.0
)
bot.run(constants.Bot.token)
