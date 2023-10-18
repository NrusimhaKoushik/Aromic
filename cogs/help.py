import discord, math, random
from discord.ext import commands

prefix = '^'

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def help(self, ctx):
        "Get commands list"
        embed = discord.Embed(title = 'Command List', description = '**Aromic** always at your service.\nHere is the Commands list!', color = discord.Color.random())
        embed.add_field(name='🤗 | Actions', value='`pat`, `kill`, `slap`, `highfive`, `hug`, `spank`, `forekiss`, `kiss`, `smile`, `bully`, `cry`, `blush`, `blow`', inline = False)
        embed.add_field(name='👹 | Anime', value='`animesearch`, `animenews`', inline = False)
        embed.add_field(name='💰 | Economy', value='`create`, `beg`, `balance`, `deposit`, `withdraw`, `daily`, `give`, `delete`', inline = False)
        embed.add_field(name='🥳 | Fun', value='`joke`, `meme`, `dog`, `cat`, `virus`, `hack`, `emojify`', inline = False)
        embed.add_field(name='🎲 | Games', value='`findimposter`, `tictactoe`, `hangman`, `rps`', inline = False)
        embed.add_field(name='ℹ️  | Info',value='`ping`, `botinfo`, `help`, `uptime`', inline=False)
        embed.add_field(name='📊 | Level System', value='`level`, `rank`, `serverleaderboard`, `globalleaderboard`', inline = False)
        embed.add_field(name='🔨 | Moderation', value='`kick`, `ban`, `unban`, `mute`, `unmute`, `purge`', inline = False)
        embed.add_field(name='🎵 | Music', value='`join`, `disconnect`, `play`, `stop`, `pause`, `resume`, `volume`, `skip`, `queue`, `removesong`', inline = False)
        embed.add_field(name='🔎 | Search', value='`lang`, `wiki`, `imgsearch`, `pokemon`', inline = False)
        embed.add_field(name='🌌 | Space', value='`apod`', inline = False)
        embed.add_field(name='🛠️ | Utility', value='`afk`, `membercount`, `avatar`, `slowmode`, `userinfo`, `serverinfo`, `addrole`, `removerole`, `lock`, `unlock`, `timer`', inline = False)
        embed.add_field(name='📺 | Youtube',value='`ytsearch`, `ytchannel`, `trending`', inline=False)
        embed.set_footer(text="Note: If you wanna create an account for economy, use /create")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
