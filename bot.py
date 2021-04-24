from pathlib import Path
import yaml
import discord
import asyncio
import constants
from secrets import randbelow
from discord.errors import NotFound, HTTPException

allowed_roles = [discord.Object(id_) for id_ in constants.MODERATION_ROLES]
filename = 'stats.yml'


class MoocahBot(discord.Client):
    """A simplistic bot that has a 0.01% change of responding to any message with 'cunt.'"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False

        # load stats from statfile
        # Check if the file exists, create if it not
        file = Path(filename)
        if not file.exists():
            print(f"Creating {filename}")
            file.touch()
            self.data = {}
        else:
            # load data
            with open(filename, encoding="UTF-8") as f:
                self.data = yaml.safe_load(f)

    async def on_ready(self):
        print('ready!')

    async def on_message(self, msg: discord.Message) -> None:
        if msg.author.bot:
            return

        # if msg.content == '.mstats':
        #     await msg.channel.send(f'{len(self.data)} cunts have been told off.')

        if msg.content == '.mrank':
            await self.display_rank(msg)

        elif msg.content.startswith('.m'):
            if not any(role.id in constants.MODERATION_ROLES for role in msg.author.roles):
                msg.channel.send("Permission Denied.")
                return

            if msg.content == '.m':
                self.active = not self.active
                if not self.active:
                    emote = constants.Emojis.status_offline
                else:
                    emote = constants.Emojis.status_online
                await msg.channel.send(f'Toggled to {emote}')

            elif msg.content.startswith('.mset'):
                await self.set_stats(msg)

            # elif msg.content.startswith('.mid'):
            #     await self.get_ids(msg)

        elif self.active:
            await self.roll_cunt(msg)

    async def set_stats(self, msg: discord.Message):
        _id = msg.mentions[0].id
        name = msg.mentions[0].display_name
        new_count = int(msg.content.split(' ')[1])  # .mset 5
        res = f"Target:  {name}  (`{_id}`) "
        if _id in self.data:
            res += f"Before: {self.data[_id]}    After: {new_count}"
        else:
            res += f"Before: NULL    After: {new_count}"
        test = await msg.channel.send(res)
        await test.add_reaction(constants.Emojis.status_online)

        def check(reaction, user):
            return user == msg.author and str(reaction.emoji) == constants.Emojis.status_online
        try:
            reaction, user = await self.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await test.delete()
        else:
            self.data[_id] = new_count
            # save to disk
            with open(filename, 'w', encoding="UTF-8") as f:
                yaml.dump(self.data, f)

    async def display_rank(self, msg: discord.Message):
        rank = await self.get_rank()
        rank_str = '\n'.join([f'**({f"{i+1}".rjust(2, "0")})**: ({c[1]}) {c[0]}' for i, c in enumerate(rank.items())])
        await msg.channel.send(rank_str)

    async def get_rank(self):
        # replace ids with names
        rank_named = {}
        for _id, count in self.data.items():
            user = self.get_user(_id)
            if user:
                name = user.display_name
            else:
                try:
                    name = await self.fetch_user(_id).display_name
                except (NotFound, HTTPException):
                    name = f'{_id}'
            rank_named[name] = count

        # sort
        return dict(sorted(rank_named.items(), key=lambda item: item[1], reverse=True))

    async def roll_cunt(self, msg: discord.Message):
        roll = randbelow(1000)
        if not roll:
            await msg.channel.send(f'{msg.author.mention} Cunt.')
            self.data[msg.author.id] += 1
            # save to disk
            with open(filename, 'w', encoding="UTF-8") as f:
                yaml.dump(self.data, f)


bot = MoocahBot(
    activity=discord.Activity(type=discord.ActivityType.watching, name='You'),
    max_messages=10000,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=allowed_roles),
    guild_ready_timeout=10.0
)
bot.run(constants.Bot.token)
