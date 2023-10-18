import discord, math, random
from discord.ext import commands

prefix = '^'

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

# class Select(discord.ui.Select):
#     def __init__(self):
#         options=[
#             discord.SelectOption(label="Actions", emoji = '🤗', description = 'Get action commands.'),
#             discord.SelectOption(label="Anime", emoji = '👹', description = 'Get anime related commands.'),
#             discord.SelectOption(label="Economy", emoji = '💰', description = 'Get economy commands.'),
#             discord.SelectOption(label="Fun", emoji = '🥳', description = 'Just fun commands.'),
#             discord.SelectOption(label="Games", emoji = '🎲', description = 'Get entertain with Game commands.'),
#             discord.SelectOption(label="Info", emoji = 'ℹ️', description = 'Get bot related commands.'),
#             discord.SelectOption(label="Levelling System", emoji = '📊', description = 'Get levelling system commands.'),
#             discord.SelectOption(label="Moderation", emoji = '🔨', description = 'Get moderation commands.'),
#             discord.SelectOption(label="Utility", emoji = '🛠️', description = 'Get utility commands.'),
#             discord.SelectOption(label="Search",  emoji = '🔍', description = 'Get multiple search commands.'),
#             discord.SelectOption(label="Youtube", emoji = '📺', description = 'Get youtube related commands.')
#         ]

#         super().__init__(placeholder="Select an command category ",options=options)

#     async def callback(self, interaction: discord.Interaction):
#         if self.values[0] == 'Actions':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n### 🤗 | Actions', color = discord.Color.random())
#             embed.add_field(name='', value=f'`{prefix}action pat` - Get pat gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action kill` - Get killing gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action hug` - Get hugging gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action slap` - Get slapping gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action highfive` - Get highfive gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action smile` - Get smiling gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action cry` - Get cry gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action forekiss` - Get forekiss gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action kiss` - Get kissing gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action spank` - Get spank gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action blow` - Get kicking gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action bully` - Get bullying gifs', inline = False)
#             embed.add_field(name='', value=f'`{prefix}action blush` - Get blushing gifs', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Anime':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n### 👺 | Anime', color = discord.Color.random())
#             embed.add_field(name='', value=f'`{prefix}animesearch` - Search about anime.', inline = False)
#             embed.add_field(name='', value=f'`{prefix}image` - Get your favourite anime character.', inline = False)
#             embed.add_field(name='', value=f'`{prefix}animenews` - Know about top trending news about anime.', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Economy':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='💰 | Economy', value='`create`, `beg`, `balance`, `deposit`, `withdraw`, `give`, `account`', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Fun':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='🥳 | Fun', value='`meme`, `dog`, `cat`, `virus`, `hack`, `emojify`', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Games':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='🎲 | Games', value='`findimposter`, `tictactoe`, `hangman`, `8ball`, `rps`', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Info':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='ℹ️  | Info',value='`ping`, `botinfo`, `help`, `uptime`', inline=False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Levelling System':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n### 📊 | Levelling System', color = discord.Color.random())
#             embed.add_field(name='', value=f'`{prefix}level` - Get your server level rank.', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Moderation':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='🔨 | Moderation', value='`kick`, `ban`, `unban`, `mute`, `unmute`, `purge`', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Utility':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='🛠️ | Utility', value='`afk`, `membercount`,`avatar`, `slowmode`, `userinfo`, `serverinfo`, `addrole`, `removerole`, `lock`, `unlock`, `timer`', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Search':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='🔎 | Search', value='`lang`, `wiki`, `googlesearch`, `imgsearch`, `votecheck`', inline = False)
#             await interaction.response.edit_message(embed=embed)

#         elif self.values[0] == 'Youtube':
#             embed = discord.Embed(title = 'Aromic Help', description = f'My command prefix is `{prefix}`.\n', color = discord.Color.random())
#             embed.add_field(name='📺 | Youtube',value='`ytsearch`, `ytchannel`, `trending`', inline=False)
#             await interaction.response.edit_message(embed=embed)


# class SelectView(discord.ui.View):
#     def __init__(self, *, timeout = 180):
#         super().__init__(timeout=timeout)
#         self.add_item(Select())

# class PaginationView(discord.ui.View):
#     current_page : int = 1
#     sep : int = 5

#     def create_embed(self, data):
#         embed = discord.Embed(title="Commands List")
#         embed.set_footer(text=f' {self.current_page} / {math.ceil(len(self.data) / self.sep)}')
#         for item in data:
#             embed.add_field(name=item['label'], value=item['item'], inline=False)
#         return embed

#     async def send(self, ctx):
#         self.message = await ctx.send(view=self)
#         await self.update_message(self.data[:self.sep])

#     async def update_message(self,data):
#         self.update_buttons()
#         await self.message.edit(embed=self.create_embed(data), view=self)

#     def update_buttons(self):
#         if self.current_page == 1:
#             self.first_page_button.disabled = True
#             self.prev_button.disabled = True
#             self.first_page_button.style = discord.ButtonStyle.gray
#             self.prev_button.style = discord.ButtonStyle.gray
#         else:
#             self.first_page_button.disabled = False
#             self.prev_button.disabled = False
#             self.first_page_button.style = discord.ButtonStyle.green
#             self.prev_button.style = discord.ButtonStyle.primary

#         if self.current_page == math.ceil(len(self.data) / self.sep):
#             self.next_button.disabled = True
#             self.last_page_button.disabled = True
#             self.last_page_button.style = discord.ButtonStyle.gray
#             self.next_button.style = discord.ButtonStyle.gray
#         else:
#             self.next_button.disabled = False
#             self.last_page_button.disabled = False
#             self.last_page_button.style = discord.ButtonStyle.green
#             self.next_button.style = discord.ButtonStyle.primary

#     def get_current_page_data(self):
#         self.current_page == math.ceil(len(self.data) / self.sep)
#         until_item = self.current_page * self.sep
#         from_item = until_item - self.sep
#         return self.data[from_item:until_item]


#     @discord.ui.button(label="|<",
#                        style=discord.ButtonStyle.green)
#     async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
#         await interaction.response.defer()
#         self.current_page = 1

#         await self.update_message(self.get_current_page_data())

#     @discord.ui.button(label="<",
#                        style=discord.ButtonStyle.primary)
#     async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
#         await interaction.response.defer()
#         self.current_page -= 1
#         await self.update_message(self.get_current_page_data())

#     @discord.ui.button(label=">",
#                        style=discord.ButtonStyle.primary)
#     async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
#         await interaction.response.defer()
#         self.current_page += 1
#         await self.update_message(self.get_current_page_data())

#     @discord.ui.button(label=">|",
#                        style=discord.ButtonStyle.green)
#     async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
#         await interaction.response.defer()
#         self.current_page = math.ceil(len(self.data) / self.sep)
#         await self.update_message(self.get_current_page_data())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
#     @commands.command()
#     async def paginate(self, ctx):
#         data = [

#         ]

#         for i in range(1,15):
#             data.append({
#                 "label": "User Event",
#                 "item": f"User {i} has been added"
#             })

#         pagination_view = PaginationView(timeout=None)
#         pagination_view.data = data
#         await pagination_view.send(ctx)

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
        embed.add_field(name='🎲 | Games', value='`findimposter`, `tictactoe`, `hangman`, `8ball`, `rps`', inline = False)
        embed.add_field(name='ℹ️  | Info',value='`ping`,`botinfo`, `help`, `uptime`', inline=False)
        embed.add_field(name='📊 | Level System', value='`level`, `rank`, `serverleaderboard`, `globalleaderboard`', inline = False)
        #embed.add_field(name='🥳 | Fun', value='`calc`, `dog`, `cat`, `virus`, `time`, `thank`, `hack`, `profile`, `meme`', inline = False) 
        #embed.add_field(name='🎉 | Giveaway', value='`gstart`, `reroll`', inline = False)
        embed.add_field(name='🔨 | Moderation', value='`kick`, `ban`, `unban`, `mute`, `unmute`, `purge`', inline = False)
        embed.add_field(name='🎵 | Music', value='`join`, `disconnect`, `play`, `stop`, `pause`, `resume`, `volume`, `skip`, `queue`, `removesong`', inline = False)
        embed.add_field(name='🔎 | Search', value='`lang`, `wiki`, `imgsearch`, `pokemon`', inline = False)
        embed.add_field(name='🌌 | Space', value='`apod`', inline = False)
        embed.add_field(name='🛠️ | Utility', value='`afk`, `membercount`, `avatar`, `slowmode`, `userinfo`, `serverinfo`, `addrole`, `removerole`, `lock`, `unlock`, `timer`', inline = False)
        embed.add_field(name='📺 | Youtube',value='`ytsearch`, `ytchannel`, `trending`', inline=False)
        embed.set_footer(text="Note: If you wanna create an account for economy, use /create")
        # embed.add_field(name='❓ | Other', value='`uptime`', inline = False)
        await ctx.send(embed=embed)

    # @commands.hybrid_command()
    # async def issueder(self,ctx):
    #     embed = discord.Embed(title = 'Command List', description = '**Aromic** always at your service.\nHere is the Commands list!', color = discord.Color.random())
    #     embed.add_field(name='🤗 | Actions', value = '', inline=False)
    #     embed.add_field(name='👹 | Anime', value = '', inline=False)
    #     embed.add_field(name='💰 | Economy', value = '', inline=False)
    #     embed.add_field(name='🥳 | Fun', value = '', inline=False)
    #     embed.add_field(name='🎲 | Games', value = '', inline=False)
    #     embed.add_field(name='ℹ️ | Info', value = '', inline=False)
    #     embed.add_field(name='🔨 | Moderation', value = '', inline=False)
    #     embed.add_field(name='🔍 | Search', value = '', inline=False)
    #     embed.add_field(name='🛠️ | Utility', value = '', inline=False)
    #     embed.add_field(name='📺 | Youtube', value = '', inline=False)
    #     embed.set_thumbnail(url=self.bot.user.display_avatar)
    #     embed.set_footer(text = 'Select the options in the menu to check the commands.')
        # await ctx.send(embed=embed, view = SelectView())
        # select = Select(options=[
        #     discord.SelectOption(label="Actions", emoji = '🤗', description = 'Get action commands.'),
        #     discord.SelectOption(label="Anime", emoji = '👹', description = 'Get anime related commands.'),
        #     discord.SelectOption(label="Economy", emoji = '💰', description = 'Get economy commands.'),
        #     discord.SelectOption(label="Fun", emoji = '🥳', description = 'Just fun commands.'),
        #     discord.SelectOption(label="Games", emoji = '🎲', description = 'Get entertain with Game commands.'),
        #     discord.SelectOption(label="Info", emoji = 'ℹ️', description = 'Get bot related commands.'),
        #     discord.SelectOption(label="Levelling System", emoji = '📊', description = 'Get levelling system commands.'),
        #     discord.SelectOption(label="Moderation", emoji = '🔨', description = 'Get moderation commands.'),
        #     discord.SelectOption(label="Utility", emoji = '🛠️', description = 'Get utility commands.'),
        #     discord.SelectOption(label="Search",  emoji = '🔍', description = 'Get multiple search commands.'),
        #     discord.SelectOption(label="Youtube", emoji = '📺', description = 'Get youtube related commands.')
        # ])

        # async def my_callback(interaction):
        #     embed = discord.Embed(title = 'Command List', description = '**Aromic** always at your service.\nHere is the Commands list!', color = discord.Color.random())
        #     embed.set_thumbnail(url = self.bot.user.display_avatar)

        #     if select.values[0] == 'Actions':
        #         embed.add_field(name='🤗 | Actions', value='`pat`, `kill`, `slap`, `highfive`, `hug`, `spank`, `forekiss`, `kiss`, `smile`, `bully`, `cry`, `blush`, `blow`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Anime':
        #         embed.add_field(name='👹 | Anime', value='`animesearch`, `image`, `animenews`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Economy':
        #         embed.add_field(name='💰 | Economy', value='`create`, `beg`, `balance`, `deposit`, `withdraw`, `give`, `account`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Fun':
        #         embed.add_field(name='🥳 | Fun', value='`meme`, `dog`, `cat`, `virus`, `hack`, `emojify`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Games':
        #         embed.add_field(name='🎲 | Games', value='`findimposter`, `tictactoe`, `hangman`, `8ball`, `rps`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Info':
        #         embed.add_field(name='ℹ️  | Info',value='`ping`, `botinfo`, `help`, `uptime`', inline=False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Level System':
        #         embed.add_field(name='📊 | Level System', value='`level`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Moderation':
        #         embed.add_field(name='🔨 | Moderation', value='`kick`, `ban`, `unban`, `mute`, `unmute`, `purge`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Utility':
        #         embed.add_field(name='🛠️ | Utility', value='`afk`, `membercount`,`avatar`, `slowmode`, `userinfo`, `serverinfo`, `addrole`, `removerole`, `lock`, `unlock`, `timer`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Search':
        #         embed.add_field(name='🔎 | Search', value='`lang`, `wiki`, `googlesearch`, `imgsearch`, `votecheck`', inline = False)
        #         await interaction.response.send_message(embed=embed)
        #     elif select.values[0] == 'Youtube':
        #         embed.add_field(name='📺 | Youtube',value='`ytsearch`, `ytchannel`, `trending`', inline=False)
        #         await interaction.response.send_message(embed=embed)

        # select.callback = my_callback
        # view = View()
        # view.add_item(select)

        # embed = discord.Embed(title = 'Command List', description = '**Aromic** always at your service.\nHere is the Commands list!', color = discord.Color.random())
        # embed.add_field(name='🤗 | Actions', value = '', inline=False)
        # embed.add_field(name='👹 | Anime', value = '', inline=False)
        # embed.add_field(name='💰 | Economy', value = '', inline=False)
        # embed.add_field(name='🥳 | Fun', value = '', inline=False)
        # embed.add_field(name='🎲 | Games', value = '', inline=False)
        # embed.add_field(name='ℹ️ | Info', value = '', inline=False)
        # embed.add_field(name='🔨 | Moderation', value = '', inline=False)
        # embed.add_field(name='🔍 | Search', value = '', inline=False)
        # embed.add_field(name='🛠️ | Utility', value = '', inline=False)
        # embed.add_field(name='📺 | Youtube', value = '', inline=False)
        # embed.set_thumbnail(url=self.bot.user.display_avatar)
        # embed.set_footer(text = 'Select the options in the menu to check the commands.')
        # await ctx.send(embed = embed, view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))