import discord
import random, json
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        guild = message.guild

        if author.bot:
            return

        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp, level, max_xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            data = await cursor.fetchone()

            if not data:
                await cursor.execute("INSERT INTO levels (level, xp, max_xp, user, guild) VALUES (?, ?, ?, ?, ?)", (0, 0, 100, author.id, guild.id,))
                await self.bot.db.commit()
            else:
                xp = data[0]
                level = data[1]
                max_xp = data[2]

                if level < 5:
                    xp += random.randint(1, 5)
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
                else:
                    rand = random.randint(1, (level//4))
                    if rand == 1:
                        xp += random.randint(1, 5)
                        await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))

                if xp >= max_xp:
                    newlvl = level + 1
                    new_maxxp = 50 * (level//2)
                    updated_maxxp = max_xp + new_maxxp
                    await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (newlvl, author.id, guild.id,))
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
                    await cursor.execute("UPDATE levels SET max_xp = ? WHERE user = ? AND guild = ?", (updated_maxxp, author.id, guild.id, ))
                    await message.channel.send(f"{message.author.mention} has leveled up to **{newlvl}**.")
        await self.bot.db.commit()

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def level(self, ctx, user:discord.Member = None):
        """Shows your current XP and the current level you are in."""
        if user is None:
            user = ctx.author
        guild = ctx.guild
        
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp, level, max_xp FROM levels WHERE user = ? AND guild = ?", (user.id, guild.id,))
            data = await cursor.fetchone()
            if data is None:
                await cursor.execute("INSERT INTO levels (level, xp, max_xp, user, guild) VALUES (?, ?, ?, ?, ?)", (0, 0, 100, user.id, guild.id,))
                await self.bot.commit()
                return await ctx.send(f'{user} don\'t have a levelling system profile. Try again to check the profile.')
            else:
                xp = data[0]
                level = data[1]
                maxxp = data[2]

                embed = discord.Embed(title=f'{user.name}\'s level', description=f'**XP**: {xp}/{maxxp}\n**Level**: {level}', color=discord.Color.random())
                embed.set_thumbnail(url = user.display_avatar.url)
                await ctx.send(embed = embed)
        await self.bot.db.commit()

    @commands.hybrid_command(name="rank")
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def rank(self, ctx: commands.Context, user: discord.Member = None):
        "Displays a users ranking on this server by their total XP."
        if user is None:
            user = user or ctx.author
        guild = ctx.guild

        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp, level, max_xp FROM levels WHERE user = ? AND guild = ?", (user.id, guild.id,))
            data = await cursor.fetchone()

            if not data:
                await cursor.execute("INSERT INTO levels (level, xp, max_xp, user, guild) VALUES (?, ?, ?, ?, ?)", (0, 0, 100, user.id, guild.id,))
                await self.bot.db.commit()

            xp = data[0]
            lvl = data[1]
            maxxp = data[2]

            percentage = int(((xp * 100)/ maxxp))

            if percentage < 1:
                percentage = 0
            
            ## Rank card
            background = Editor(f"zIMAGE.png")
            profile = await load_image_async(str(user.display_avatar))

            profile = Editor(profile).resize((150, 150)).circle_image()
            
            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            #you can skip this part, I'm adding this because the text is difficult to read in my selected image
            ima = Editor("zBLACK.png")
            background.blend(image=ima, alpha=.5, on_top=False)

            background.paste(profile.image, (30, 30))

            background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
            background.bar(
                (30, 220),
                max_width=650,
                height=40,
                percentage=percentage,
                fill="#ff9933",
                radius=20,
            )
            background.text((200, 40), str(user.name), font=poppins, color="#ff9933")

            background.rectangle((200, 100), width=350, height=2, fill="#ff9933")
            background.text(
                (200, 130),
                f"Level : {lvl}   "
                + f" XP : {xp} / {maxxp}",
                font=poppins_small,
                color="#ff9933",
            )

            card = discord.File(fp=background.image_bytes, filename="zCARD.png")
            await ctx.send(file=card)
        await self.bot.db.commit()

    @commands.hybrid_command(aliases=['slb','lb','leaderboard'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def serverleaderboard(self, ctx):
        """Shows the levelling leaderboard of the server"""
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT level, user FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 10", (ctx.guild.id,))
            data = await cursor.fetchall()
            msg = await ctx.send("Getting information...")
            if data:
                em = discord.Embed(title='Server Level Leaderboard')

                for i, table in enumerate(data[:3]):
                    i += 1
                    if i == 1:
                        emoji = '🥇'
                    elif i == 2:
                        emoji = '🥈'
                    elif i == 3:
                        emoji = '🥉'
                    user = await self.bot.fetch_user(table[1])
                    em.add_field(name='', value=f'{emoji} Level - `{table[0]}` | **{user.display_name}**',inline=False)

                for table in data[3:]:
                    user = await self.bot.fetch_user(table[1])
                    em.add_field(name='', value=f'▫️ Level - `{table[0]}` | **{user.display_name}**',inline=False)

                for i, table in enumerate(data):
                    i += 1
                    user = await self.bot.fetch_user(table[1])
                    if user.display_name == ctx.author.display_name:
                        em.set_footer(text=f'You position: #{i}')

                await msg.delete()
                return await ctx.send(embed=em)
            return await ctx.send("There are no users stored in the leaderboard -_-")
    
    @commands.hybrid_command(aliases=['glb'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def globalleaderboard(self, ctx):
        """Shows the global levelling leaderboard"""
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT level, user, guild FROM levels ORDER BY level DESC, xp DESC LIMIT 10")
            data = await cursor.fetchall()

            with open("data.json", "w") as file:
                file.write(json.dumps(data))

            msg = await ctx.send("Getting information...")

            if data:
                em = discord.Embed(title='Global Level Leaderboard')

                for i, table in enumerate(data[:3]):
                    i += 1
                    if i == 1:
                        emoji = '🥇'
                    elif i == 2:
                        emoji = '🥈'
                    elif i == 3:
                        emoji = '🥉'

                    user = await self.bot.fetch_user(table[1])
                    server = await self.bot.fetch_guild(table[2])
                    em.add_field(name='', value=f'{emoji} Level - `{table[0]}` | **{user.display_name}** at *{server.name}*',inline=False)

                for table in data[3:]:
                    user = await self.bot.fetch_user(table[1])
                    server = await self.bot.fetch_guild(table[2])
                    em.add_field(name='', value=f'▫️ Level - `{table[0]}` | **{user.display_name}** at *{server.name}*',inline=False)

                for i, table in enumerate(data):
                    i += 1
                    user = await self.bot.fetch_user(table[1])
                    guild = await self.bot.fetch_guild(table[2])
                    if user.display_name == ctx.author.display_name and guild.name == ctx.guild.name:
                        em.set_footer(text=f'You position: #{i}')

                await msg.delete()
                return await ctx.send(embed=em)
            return await ctx.send("There are no users stored in the leaderboard -_-")

async def setup(bot):
    await bot.add_cog(Level(bot))
