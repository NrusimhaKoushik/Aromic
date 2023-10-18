import discord, asyncio, datetime, time
from discord.ext import commands
from mongo import db
from afk import afks

global startTime
startTime = time.time()

def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occurred.'
    return result

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class MyView(discord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.expression = ""
        self.add_item(MyButton(label = "1" , style=discord.ButtonStyle.grey , row = 1))
        self.add_item(MyButton(label = "2" , style=discord.ButtonStyle.grey , row = 1))
        self.add_item(MyButton(label = "3" ,style = discord.ButtonStyle.grey , row = 1))
        self.add_item(MyButton(label = "×" , style = discord.ButtonStyle.blurple , row = 1))
        self.add_item(MyButton(label = "Exit" , style = discord.ButtonStyle.red , row = 1))
        self.add_item(MyButton(label = "4" , style = discord.ButtonStyle.grey , row = 2))
        self.add_item(MyButton(label = "5" , style = discord.ButtonStyle.grey , row = 2))
        self.add_item(MyButton(label = "6" , style = discord.ButtonStyle.grey , row = 2))
        self.add_item(MyButton(label = "÷" , style = discord.ButtonStyle.blurple , row = 2))
        self.add_item(MyButton(label = "←" , style = discord.ButtonStyle.red , row = 2))
        self.add_item(MyButton(label = "7" , style = discord.ButtonStyle.grey , row = 3))
        self.add_item(MyButton(label = "8" , style = discord.ButtonStyle.grey , row = 3))
        self.add_item(MyButton(label = "9" , style = discord.ButtonStyle.grey , row = 3))
        self.add_item(MyButton(label = "+" , style = discord.ButtonStyle.blurple , row = 3))
        self.add_item(MyButton(label = "C" , style = discord.ButtonStyle.red , row = 3))
        self.add_item(MyButton(label = "00" , style = discord.ButtonStyle.grey , row = 4))
        self.add_item(MyButton(label = "0" ,style = discord.ButtonStyle.grey , row = 4))
        self.add_item(MyButton(label = "." , style = discord.ButtonStyle.grey , row = 4))
        self.add_item(MyButton(label = "-" ,style = discord.ButtonStyle.blurple , row = 4))
        self.add_item(MyButton(label = "=" , style = discord.ButtonStyle.green , row = 4))

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't do that!", ephemeral = True)
            return False
        else:
            return True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(embed=discord.Embed(description = "⏰ __**Timeout , You can't react with the button**__" , color = discord.Colour.red()), view=self)

class MyButton(discord.ui.Button):
    async def callback(self, interaction : discord.Interaction):
        assert self.view is not None
        view: MyView = self.view
        if str(self.label) == "Exit":
            view.clear_items()
            return
        elif view.expression == 'None' or view.expression == 'An error occurred.':
            view.expression = ''
        elif str(self.label) == "←":
            view.expression = view.expression[:-1]
        elif str(self.label) == "C":
            view.expression = ' '
        elif str(self.label) == "=":
            view.expression = calculate(view.expression)
        else:
            view.expression += self.label
        
        e = discord.Embed(title=f'{interaction.user.name}\'s calculator | {interaction.user.id}', description=f"```fix\n{view.expression}```",timestamp=discord.utils.utcnow() , color = discord.Colour.green())
        await interaction.response.edit_message(view = view, embed=e , content = None)

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = db

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.has_permissions(administrator = True)
    async def setprefix(self, ctx, prefix = None):
        guild = ctx.guild
        if prefix is None:
            return await ctx.send('Please mention prefix!')
        
        m = self.db.guild.find_one({"_id": guild.id})
        pre = m["prefix"]

        if m is not None:
            self.db.guild.update_one({"prefix": pre}, {"$set": {"prefix": prefix}})
            return await ctx.send(f"Prefix changed to **{prefix}**.")
        else:
            self.db.guild.insert_one({"_id": guild.id}, {"prefix": prefix})
            return await ctx.send(f"**{prefix}** added.")
    
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.has_permissions(administrator = True)
    async def removeprefix(self, ctx):
        prefix = 'DEFAULT_PREFIX'
        guild = ctx.guild
        if prefix is None:
            return await ctx.send('Please mention prefix!')
        
        m = self.db.guild.find_one({"_id": guild.id})
        pre = m["prefix"]

        if m is not None:
            self.db.guild.update_one({"prefix": pre}, {"$set": {"prefix": prefix}})
            return await ctx.send(f"Prefix changed to **{prefix}**.")
        else:
            self.db.guild.insert_one({"_id": guild.id}, {"prefix": prefix})
            return await ctx.send(f"**{prefix}** added.")

    @commands.hybrid_command(aliases= ["buttoncal" , "bcal" , "calc" , "calculator" , "cal"])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def calculate(self,ctx):
        view = MyView(ctx)
        m = await ctx.send(content='Loading Calculator...')
        expression = 'None'
        delta = discord.utils.utcnow() + datetime.timedelta(minutes=5)
        e = discord.Embed(title=f'{ctx.author.name}\'s calculator | {ctx.author.id}', description=expression,timestamp=delta , color = discord.Colour.blurple())
        e.set_footer(text = f"The button calculator will be expired in 2 minutes")
        view.message = await m.edit(view = view, embed=e , content = None)
    
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def math(self,ctx, *, expression:str):
        calculation = eval(expression)
        embed = discord.Embed(color=discord.Colour.random())
        embed.set_author(name=f"{ctx.author}" , icon_url = f"{ctx.author.avatar.url}")
        embed.add_field(name="**Math :**" , value=f"```yaml\n {expression}```" , inline=False)
        embed.add_field(name="**Answer :**" , value=f"```Fix\n {calculation}```" , inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}"  , icon_url = f"{ctx.author.avatar.url}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(alaiases = ['pfp', 'av'],description='Shows the user profile pic')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def avatar(self, ctx, user:discord.Member=None):
        if user is None:
            user = ctx.author
        em = discord.Embed(color=discord.Color.random())
        em.set_image(url=user.display_avatar.url)
        av_button = discord.ui.Button(label='Download',url=user.display_avatar.url,emoji='⬇️')
        view = discord.ui.View()
        view.add_item(av_button)
        await ctx.send(embed=em, view=view)
    
    @commands.hybrid_command(aliases=['ar'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def addrole(self, ctx, user: discord.Member, *, role: discord.Role):
        aromic = ctx.guild.get_member(self.bot.user.id)
        if ctx.author.guild_permissions.administrator:
            if role > aromic.top_role:
                await ctx.send(f"My top role was lower than the role adding. So please do some manual work and give me hierarchy permissions to add the role to Users.")
                return
            if role in user.roles:
                await ctx.send(f'{role} already given to {user}.')
            else:
                await user.add_roles(role)
                await ctx.send(f"Added {role.mention} to {user.mention}")

    @addrole.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permissions to execute this command.')

    @commands.hybrid_command(aliases=["mc"])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def membercount(self, ctx):
      a=ctx.guild.member_count
      b=discord.Embed(title=f"MemberCount", description=a, color=discord.Color.blue())
      await ctx.send(embed=b)

    @commands.hybrid_command(aliases=['user', 'whois'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def userinfo(self, ctx, *, member:discord.Member = None):
        if member == None:
                member = ctx.message.author

        embed=discord.Embed(title="User Information", timestamp=ctx.message.created_at,colour=discord.Colour.random())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Name", value=str(member), inline=False)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name='Bot?', value=member.bot, inline=True)
        embed.add_field(name="Toprole", value=member.top_role.mention, inline=True)
        embed.add_field(name="Account Created",value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name="Joined",value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name="Boosted", value=bool(member.premium_since), inline=True)
        await ctx.send(embed=embed)
    
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def serverinfo(self, ctx):
        embed = discord.Embed(title= f"{ctx.guild.name}",color = ctx.author.color,timestamp=ctx.message.created_at)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels
        embed.set_thumbnail(url = str(ctx.guild.icon))
        embed.add_field(name = f"", value = f""":white_small_square: ID: **{ctx.guild.id}**
                        :white_small_square: Owner: <@{ctx.guild.owner_id}>
                        :white_small_square: Creation: **{ctx.guild.created_at.strftime('%a %d %B %Y, %I:%M %p UTC')}**
                        :white_small_square: Members: **{ctx.guild.member_count}** 
                        :white_small_square: Channels: **{channels}** | #️⃣ - **{text_channels}**, 🔊 - **{voice_channels}**
                        :white_small_square: Categories: **{categories}**
                        :white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}**
                        :white_small_square: Features: {', '.join(f'{x}' for x in ctx.guild.features)}
                        :white_small_square: Splash: {ctx.guild.splash}""")
        embed.set_footer(text=f'Requested by: {ctx.author.name}', icon_url=str(ctx.author.display_avatar))
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=['sm'])
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def slowmode(self, ctx, time=None):
        if time == 0 or time is None or time == '0s'or time == '0S': #Disabled slowmode
            await ctx.channel.edit(slowmode_delay=0)
            return await ctx.send(embed=discord.Embed(title="Slowmode disabled"))
        try:
            convertTimeList = {'s':1, 'm':60, 'S':1, 'M':60}
            times = int(time[:-1]) * convertTimeList[time[-1]]

            if times<0 or times>21600: #Out of range
                return await ctx.send(embed=discord.Embed(title="You cannot set a time lower than 0 seconds or greater than 21600 seconds! 0 seconds disables slowmode"))
            else: #Correct range
                await ctx.channel.edit(slowmode_delay=times)
                await ctx.send(embed=discord.Embed(title=f"Slowmode set to {time}."))
        except Exception:
            await ctx.send('**Syntax**: `^slowmode [time][s/m]`\ns - seconds\nm - minutes')

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            return await ctx.send(embed=discord.Embed(title="HA you don't have the proper perms to do that. What an L"))
        elif isinstance(error,commands.BadArgument):
            return await ctx.send(embed=discord.Embed(title="You must enter an integer."))

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def uptime(self, ctx):
        try:
            text = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
            embed = discord.Embed(color=discord.Colour.blurple())
            embed.add_field(name="The bot was online for: ", value=f":alarm_clock: {text}", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

        except Exception as e:
            embed3 = discord.Embed(title=":red_square: Error!", description="The command was unable to run successfully! ", color=0xff0000)
            embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/877796755234783273/879298565380386846/sign-red-error-icon-1.png")
            embed3.add_field(name="Error:", value=f"```{e}```", inline=False)
            embed3.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed3)
    
    @commands.hybrid_command(aliases=['deleterole', 'rr'])
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def removerole(self, ctx, user:discord.Member, role:discord.Role):
      if ctx.author.guild_permissions.administrator:
        try:
            await user.remove_roles(role)
            await ctx.send(f"Sucessfully removed {role.mention} to {user.mention}")
        except Exception as e:
            embed3 = discord.Embed(title=":red_square: Error!", description="The command was unable to run successfully! ", color=0xff0000)
            embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/877796755234783273/879298565380386846/sign-red-error-icon-1.png")
            embed3.add_field(name="Error:", value=f"```{e}```", inline=False)
            embed3.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed3)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def afk(self, ctx, *, reason = None):
        if ctx.author.id in afks.keys():
            afks.pop(ctx.author.id)
        else:
            try:
                await ctx.author.edit(nick = f"(AFK) {ctx.author.display_name}")
            except:
                pass
        afks[ctx.author.id] = reason
        embed = discord.Embed(title = ":zzz: Member AFK", description = f"{ctx.author.mention} has gone AFK",color = discord.Color.random(), timestamp = ctx.message.created_at)
        embed.set_thumbnail(url = ctx.author.display_avatar)
        embed.set_footer(text=f"{self.bot.user.name}", icon_url=str(self.bot.user.display_avatar))
        embed.add_field(name='Reason: ',value=reason)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def lock(self, ctx, channel: discord.TextChannel = None, roles: discord.Role = None):
        if channel is None:
            channel = ctx.channel
        if not roles:
            roles = [ctx.guild.default_role]
        if isinstance(channel, discord.TextChannel):
            for role in roles:
                default = channel.overwrites_for(ctx.guild.default_role)
                my_perms = channel.overwrites_for(ctx.me)
                if my_perms.send_messages != True:
                    my_perms.update(send_messages=True)
                    await channel.set_permissions(ctx.me, overwrite=my_perms)
                if default.send_messages == False:
                    return
                else:
                    default.update(send_messages=False)
        await channel.set_permissions(role, reason=f"{ctx.author.name} unlocked {channel.name}", overwrite=default)
        await ctx.send(f'Lockdown has been applied to {channel.mention}.')
       
    
    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def unlock(self, ctx, channel: discord.TextChannel = None, roles: discord.Role = None):
        if channel is None:
            channel = ctx.channel
        if not roles:
            roles = [ctx.guild.default_role]
        if isinstance(channel, discord.TextChannel):
            for role in roles:
                default = channel.overwrites_for(ctx.guild.default_role)
                my_perms = channel.overwrites_for(ctx.me)
                if my_perms.send_messages != True:
                    my_perms.update(send_messages=True)
                    await channel.set_permissions(ctx.me, overwrite=my_perms)
                if default.send_messages == True:
                    return 
                else:
                    default.update(send_messages=True)
        await channel.set_permissions(role, reason=f"{ctx.author.name} unlocked {channel.name}", overwrite=default)
        await ctx.send(f'I have removed <#{channel.id}> from Lockdown.')

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def timer(self, ctx, time):
        try:
            try:
                time = int(time)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
                time = int(time[:-1]) * convertTimeList[time[-1]]
            if time > 86400:
                await ctx.send("I can\'t do timers over a day long")
                return
            if time <= 0:
                await ctx.send("Timers don\'t go into negatives :/")
                return
            if time >= 3600:
                message = await ctx.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            elif time >= 60:
                message = await ctx.send(f"Timer: {time//60} minutes {time%60} seconds")
            elif time < 60:
                message = await ctx.send(f"Timer: {time} seconds")
            while True:
                try:
                    await asyncio.sleep(5)
                    time -= 5
                    if time >= 3600:
                        await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                    elif time >= 60:
                        await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                    elif time < 60:
                        await message.edit(content=f"Timer: {time} seconds")
                    if time <= 0:
                        await message.edit(content="Ended!")
                        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
                        break
                except:
                    break
        except:
            await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time **{time}**....")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def createembed(self,ctx):
        reactions = ['✅']
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send("Enter Title of Embed: ")
        try:
            msg = await self.bot.wait_for('message', timeout=20.0, check = check)
            title = msg.content
        except asyncio.TimeoutError:
            await ctx.channel.purge(limit=1)
            return await ctx.send("Timed Out")
        
        await ctx.send("Enter Description of Embed: ")
        try:
            msg2 = await self.bot.wait_for('message', timeout=20.0, check = check)
            description = msg2.content
        except asyncio.TimeoutError:
            await ctx.channel.purge(limit=3)
            return await ctx.send("Timed Out")

        try:
            embed = discord.Embed(title=title, description=description, color=discord.Color.random(), timestamp=ctx.message.created_at)
            embed.set_thumbnail(url = str(ctx.guild.icon))
            embed.set_footer(text=f'Added by: {ctx.author.name}', icon_url=str(ctx.author.display_avatar))
            await ctx.channel.purge(limit=5)
            await ctx.send("Fetching details..")
            await asyncio.sleep(1)
            await ctx.send("Creating Embed...")
            await ctx.channel.purge(limit=2)
            m = await ctx.send(embed=embed)
            for reaction in reactions:
                await m.add_reaction(reaction)
        except Exception:
            embed = discord.Embed(title=title, description=description, color=discord.Color.random(), timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Added by: {ctx.author.name}')
            m = await ctx.send(embed=embed)
            for reaction in reactions:
                await m.add_reaction(reaction)

async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))
