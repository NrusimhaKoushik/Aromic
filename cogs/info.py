import discord
from discord.ext import commands
import time
import asyncio
import psutil

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def ping(self,ctx):
        """Pong!"""
        now = time.time()
        msg = await ctx.send(embed=discord.Embed(title=":ping_pong:  **WebSocket (API) latency: ``Pinging...`` | Bot latency: ``Pinging...``**", color=ctx.author.color))
        api_latency = int(self.bot.latency*1000)
        ping = int((time.time() - now)*100)
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title=f":ping_pong:  **WebSocket (API) latency: ``{api_latency}ms`` | Bot latency: ``{ping}ms``**", color=ctx.author.color))

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def botinfo(self, ctx):
        "What you do with bot information? Dont try to sell it.."
        values = psutil.virtual_memory()
        val2 = values.available * 0.001
        val3 = val2 * 0.001
        val4 = val3 * 0.001

        values2 = psutil.virtual_memory()
        value21 = values2.total
        values22 = value21 * 0.001
        values23 = values22 * 0.001
        values24 = values23 * 0.001

        embedve = discord.Embed(
            title="Bot Info", color=0x9370DB)
        embedve.add_field(
            name="Bot Latency", value=f"Bot latency - `{round(self.bot.latency * 1000)}`ms", inline=False)
        embedve.add_field(name='Hosting Stats', value=f'Cpu usage- {psutil.cpu_percent(1)}%'
                          f'\n(Actual Cpu Usage May Differ)'
                          f'\n'

                          f'\nNumber OF Cores - {psutil.cpu_count()} '
                          f'\nNumber of Physical Cores- {psutil.cpu_count(logical=False)}'
                          f'\n'

                          f'\nTotal ram- {round(values24, 2)} GB'
                          f'\nAvailable Ram - {round(val4, 2)} GB')
        embedve.set_thumbnail(url=self.bot.user.display_avatar)
        await ctx.send(embed=embedve)

    @commands.hybrid_command(aliases=['guilds'], invoke_without_command=True)
    @commands.is_owner()
    @commands.before_invoke(record_usage)
    async def servers(self, ctx):
        "Returns the server count and server names bot was in."
        user = ctx.author
        guild_id = '\n'.join(str(guild.id) for guild in self.bot.guilds)
        guild_name = '\n'.join(str(guild.name) for guild in self.bot.guilds)
        embed = discord.Embed(title='Servers I Joined', description=f'Iam at **{len(self.bot.guilds)}** servers.')
        await user.send(f'\n{guild_name}')
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def invite(self, ctx):
        "Invite me!"
        av_button = discord.ui.Button(label='Invite Now!', url = 'BOT_INVITE_URL')
        view = discord.ui.View()
        view.add_item(av_button)
        await ctx.send('Invite me to your server.\nYou can also click invite button on my profile!')
        await ctx.send(view=view)
    
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def support(self, ctx):
        "Do you have queries about me? Join support server now!"
        av_button = discord.ui.Button(label='Support Server!', url = 'SUPPORT_SERVER_URL')
        view = discord.ui.View()
        view.add_item(av_button)
        await ctx.send('You can join my support server by clicking button below.\nYou can report bugs, request new features.')
        await ctx.send(view=view)
    
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def vote(self, ctx):
        "Vote me please!"
        av_button = discord.ui.Button(label='Vote me at DBL!', url = 'DBL_VOTE_LINK')
        av_but = discord.ui.Button(label="Vote me at Top.gg!", url = "TOPGG_VOTE_LINK")
        view = discord.ui.View()
        view.add_item(av_button)
        view.add_item(av_but)
        embed = discord.Embed(title='Vote for Aromic', description='Vote me at **DiscordBotList** & **Top.gg** by the following links below.', color = ctx.author.color)
        await ctx.send(embed=embed, view=view)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
