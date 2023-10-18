import discord, os, random, asyncio
from typing import *
from config import *
import logging
from discord.ext import commands, tasks
from mongo import db
import aiosqlite

logger = logging.getLogger("bot")

async def getprefix(bot, message):
    s = db.guild.find_one({"_id": message.guild.id})
    if s is not None:
        return s["prefix"]
    else:
        db.guild.insert_one({
            "_id": message.guild.id,
            "prefix": "^"
            })
        return "^"

intents = discord.Intents.default()
intents.message_content=True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=getprefix, intents=intents, help_command=None)
        self.synced=False
    
    async def on_ready(self):
        channel = bot.get_channel(1133036643499130981)
        await bot.wait_until_ready()
        await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f'{len(bot.guilds)} Servers.'))

        bot.db = await aiosqlite.connect("level.db")
        await asyncio.sleep(3)
        async with bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, max_xp INTEGER, user INTEGER, guild INTEGER)")
        await bot.db.commit()
        # print("Databases Activated!!")

        if not self.synced:
            await bot.tree.sync()
            self.synced = True
        logger.info(f"User: {bot.user} (ID: {bot.user.id}) was Online!")
        # print(f"Logged in as {bot.user}")
        await channel.send("Systems Online!!")

        # my_background_task.start()

    async def setup_hook(self):
        for name in os.listdir('cogs'):
            if name.endswith('.py'):
                try:
                    await self.load_extension(f"cogs.{name[:-3]}")
                    print('Loaded: cogs.{}'.format(name[:-3]))
                except Exception as error:
                    print(f'cogs.{name[:-3]} cannot be loaded. [{error}]')

bot = MyBot()

@tasks.loop(seconds=10.0)
async def my_background_task():
    """Will loop every 60 seconds and change the bots presence"""
    # total_members = 0
    # for guild in bot.guilds:
    #     total_members += guild.member_count
    # stat = [
    #     f'{total_members} Peps with shrewd powers',
    #     f"{len(bot.guilds)} Servers"
    #     ]
    # rand_status = random.choice(stat)
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(name = f"{len(bot.guilds)} Servers"))

@bot.command()
async def sync(ctx, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

# Works like:
# !sync -> global sync
# !sync ~ -> sync current guild
# !sync * -> copies all global app commands to current guild and syncs
# !sync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
# !sync id_1 id_2 -> syncs guilds with id 1 and 2
try:
    bot.run(TOKEN, root_logger=True)
except:
    os.system("kill 1")