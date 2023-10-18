import discord, datetime, requests, string
from discord.ext import commands
from aiohttp import ClientSession
from config import APOD_API

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Space(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def apod(self, ctx, *, date = None):
        """Get the Astronomy Picture of the Day"""
        if date is None:
            date = datetime.date.today()
        elif date == 'today':
            date = datetime.date.today()
        elif date == 'yesterday':
            date =  datetime.date.today() - datetime.timedelta(days=1)
        elif date == 'tommorow':
            date = datetime.datetime.today().strftime("%b %d, %Y")
            return await ctx.send(f'Date must be between Jun 16, 1995 and {date}.')
        
        await ctx.send("Collecting APOD data from NASA..")

        async with ClientSession() as resp:
            async with resp.get(f'https://api.nasa.gov/planetary/apod?api_key={APOD_API}&date={date}') as response:
                data = await response.json()
                try:
                    title = data['title']
                    apod_url = data['hdurl']
                    description = data['explanation']
                    date = data['date']

                    date_split = date.split("-")

                    date_list = []
                    for i in date_split:
                        datei = int(i)
                        date_list.append(datei)
                    
                    for i in range(0,3):
                        year, month, date = date_list

                    format_date = datetime.date(int(year), int(month), int(date))
                    name = format_date.strftime("%B %d, %Y")

                    # dt = datetime.datetime.now()
                    # name = f"<t:{int(dt.timestamp())}:D>"

                    embed = discord.Embed(title=title, description=f'{description}', color = discord.Color.random())
                    embed.set_author(name=f'Astronomy Picture Of the Day')
                    embed.set_image(url=apod_url)
                    embed.set_footer(text=f"Requested APOD Date: {name}")
                    await ctx.channel.purge(limit=1)
                    await ctx.send(embed=embed)

                except Exception as e:
                    code = data["code"]
                    if code is not None:
                        message = data['msg']
                        embed = discord.Embed(title='⛔ Error Code: 400', description=message, color= discord.Color.red())
                        embed.set_footer(text='Date Format must be in YYYY-MM-DD. Try again')
                        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Space(bot))