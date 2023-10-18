import discord
import aiosqlite
from discord.ext import commands
from discord.utils import get
from discord.channel import TextChannel
from mongo import db
from afk import afks

GENERAL_CHANNEL_NAMES = {"welcome", "general", "lounge", "chat", "talk", "main", "general-chat"}

def remove(afk):
    if "(AFK)" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            channel = self.bot.get_channel("ERROR_LOG_CHANNEL_ID")

            if isinstance(error, commands.MissingRequiredArgument):
                missing = error.param.name
                await ctx.send(f":no_entry: `{missing}` is a required argument that\'s missing.", delete_after=4)
            
            if isinstance(error, commands.ExtensionNotFound):
                await ctx.send(f":no_entry: ```{error}```", delete_after = 4)
            
            if isinstance(error, commands.NoPrivateMessage):
                await ctx.send(":no_entry: This Message cannot be used in Private Message!", delete_after=4)
            
            if isinstance(error, commands.GuildNotFound):
                await ctx.send(":no_entry: Guild Not Found!", delete_after=4)

            if isinstance(error, commands.ChannelNotFound):
                await ctx.send(":no_entry: Channel Not Found", delete_after=4)

            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f":no_entry: `{error}`", delete_after=5)
            
            if isinstance(error, discord.Forbidden):
                await ctx.send(":no_entry: I'm not allowed to do that", delete_after=4)
            
            if isinstance(error, commands.MemberNotFound):
                await ctx.send(":no_entry: Member Not Found!", delete_after = 4)
            
            if isinstance(error, commands.TooManyArguments):
                await ctx.send(":no_entry: Too many arguments provided. Please try again!", delete_after=4)
            
            if isinstance(error, commands.NotOwner):
                await ctx.send(":no_entry: Sorry I dont have permission to execute that command!", delete_after=4)
            
            if isinstance(error, commands.MessageNotFound):
                await ctx.send(":no_entry: Message not Found in the Channel!", delete_after=4)
            
            if isinstance(error, commands.CommandOnCooldown):
                day = round(error.retry_after/86400)
                hour = round(error.retry_after/3600)
                minute = round(error.retry_after/60)
                if day > 0:
                    await ctx.send(':no_entry: This command has a cooldown, be sure to wait for **'+str(day)+ " day(s)**", delete_after=4)
                elif hour > 0:
                    await ctx.send(':no_entry: This command has a cooldown, be sure to wait for **'+str(hour)+ " hour(s)**", delete_after=4)
                elif minute > 0:
                    await ctx.send(':no_entry: This command has a cooldown, be sure to wait for **'+str(minute)+" minute(s)**", delete_after=4)
                else:
                    await ctx.send(f':no_entry: This command has a cooldown, be sure to wait for **{error.retry_after:.2f} second(s)**', delete_after=4)

            if isinstance(error, commands.MissingPermissions):
                if len(error.missing_perms) == 1:
                    perms = ''.join(error.missing_perms)
                else:
                    perms = ', '.join(error.missing_perms)
                await ctx.send(f":no_entry: You need the following perms: `{perms}` to execute the Command.", delete_after = 4)

            if isinstance(error, commands.BotMissingPermissions):
                if len(error.missing_perms) == 1:
                    perms = ''.join(error.missing_perms)
                else:
                    perms = ', '.join(error.missing_perms)
                await ctx.reply(f":no_entry: I need the following perms: `{perms}` to execute the Command.", delete_after=4)
                
            await channel.send(f"Error Occured at **{ctx.guild.name}**:\n```{str(error)}```")
        except:
            await channel.send(f"Error Occured at **{ctx.guild.name}**:\n```{str(error)}```")

    # async def banknote(self,user,name):
    #     async with self.bot.db.cursor() as cursor:
    #         await cursor.execute('SELECT banknote FROM bank WHERE user = ?', (user,))
    #         data = await cursor.fetchone()
    #         await cursor.execute('UPDATE bank SET banknote = ? WHERE user = ?', (name, user,))
    #     await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick = remove(message.author.display_name))
            except:
                pass
            await message.channel.send(f'Welcome back {message.author.mention}, I removed your AFK')
        
        for id, reason in afks.items():
            member = await message.guild.fetch_member(id)
            for user_mentioned in message.mentions:
                if user_mentioned.name == member.name:
                    await message.reply(f"**{member.display_name}** is AFK | Reason : **{reason}**")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel2 = self.bot.get_channel("ERROR_LOG_CHANNEL_ID")
        channel3 = self.bot.get_channel("JOIN_INFO_CHANNEL_ID")
        priority_channels = []
        channels = []
        for channel in guild.channels:
            if channel == guild.system_channel or any(
                x in channel.name for x in GENERAL_CHANNEL_NAMES
            ):
                priority_channels.append(channel)
            else:
                channels.append(channel)
        channels = priority_channels + channels
        try:
            channel = next(
                x
                for x in channels
                if isinstance(x, TextChannel) and x.permissions_for(guild.me).send_messages
            )

            embed = discord.Embed(title="",description=f"Hey Users. I am **Aromic**.\n\nType `^help` for more Information.\n\n**Support Server** for support.", color = discord.Color.blurple())
            embed.set_footer(text="Enjoy the commands!",)
            embed.set_thumbnail(url=self.bot.user.display_avatar)
            await channel.send(embed=embed)
            embed2 = discord.Embed(title = 'Joined New Server! 🎉', description = f'I Joined at **{guild.name}**', color = discord.Color.random())
            await channel3.send(embed=embed2)
        except Exception as e:
            await channel2.send(f'Error occured at `**{guild.name}**`: `{e}`')

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
