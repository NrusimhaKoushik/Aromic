import discord
import datetime
import asyncio
from discord.ext import commands

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def purge(self, ctx, amount=3):
        "Delete amount of message in a channel."
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Deleted `{amount}` Messages!')
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)

    @commands.hybrid_command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def kick(self, ctx, user: discord.Member, *, reason = None):
        "Kick someone from your server!"
        try:
            if user == ctx.author:
                await ctx.send("You can't kick yourself. Self-harm is bad.")
                return
            elif ctx.guild.me.top_role < user.top_role or user == ctx.guild.owner:
                await ctx.send("Sorry it aganist the Server rules.")
                return
            elif not reason:
                await user.kick()
                await ctx.send(f"**{user}** has been kicked for **no reason**.")
            else:
                await user.kick(reason=reason)
                await ctx.send(f"**{user}** has been kicked for **{reason}**.")
        except discord.Forbidden:
                return await ctx.send("Sorry it's aganist the Hierarchy rules.")

    @commands.hybrid_command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def ban(self, ctx, member:discord.Member, *, reason=None):
        "Ban someone from your server!"
        try:
            if member == ctx.author:
                await ctx.send("You can't ban yourself. Self-harm is bad.")
                return
            elif not reason:
                await member.ban()
                await ctx.send(f"**{member}** has been banned for **no reason**.")
            else:
                await member.ban(reason=reason)
                await ctx.send(f"**{member}** has been banned for **{reason}**.")
        except discord.Forbidden:
            return await ctx.send("Sorry it's aganist the Hierarchy rules.")

    @commands.hybrid_command(aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def unban(self, ctx, user):
        "Unbans a previously banned person."
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

            await ctx.send(f'Unbanned {user.mention}')
            return
            

    @commands.hybrid_command()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def mute(self, ctx, member:discord.Member, amount = None):
        "Mute the annoying users."
        convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
        time = int(amount[:-1]) * convertTimeList[amount[-1]]
        
        if member == ctx.author:
            return await ctx.send("You can't mute yourself!")
        if member == self.bot.user:
            return await ctx.send("You can't make me mute myself!")
        if amount is None:
            return await ctx.send("Specify Time to Mute!!")
        
        role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
        if not role: # checks if there is muted role
            try: # creates muted role 
                muted = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                    await channel.set_permissions(muted, send_messages=False, connect=False)
            except discord.Forbidden:
                return await ctx.send("I lack of `MANAGE SERVER`/ `MANAGE CHANNELS`/ `MANAGE ROLES` permission in my role. Please check it and try again") # self-explainatory
            await member.add_roles(muted) # adds newly created muted role
            await ctx.send(f"{member.mention} has been Muted.")
            await asyncio.sleep(time)
            await member.remove_roles(muted)
            await ctx.send(f'{member.mention} has been Unmuted.')
        else:
            await member.add_roles(role) # adds already existing muted role
            await ctx.send(f"{member.mention} has been Muted.")
            await asyncio.sleep(time)
            await member.remove_roles(role)
            await ctx.send(f'{member.mention} has been Unmuted.')
    
    @commands.hybrid_command(aliases=['um'])
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def unmute(self, ctx, member: discord.Member):
        "Unmutes a user!"
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted")

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))