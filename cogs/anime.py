import animec
import discord
import datetime
from aiohttp import ClientSession
from discord.ext import commands

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Anime(commands.Cog):
    """Anime commmands for weebs"""
    def __init__(self,bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def animesearch(self,ctx,*,query):
        "Search any Anime info regarding Rating, Episodes, Status etc.."
        try:
            anime = animec.Anime(query)
        except:
            await ctx.send(embed=  discord.Embed(description = "No corresponding Anime is found for the search query",color = discord.Color.red()))
            return
        embed = discord.Embed(title = anime.title_english,url = anime.url,description = f"{anime.description[:200]}...",color = discord.Color.random())
        embed.add_field(name = "Episodes",value = str(anime.episodes))
        embed.add_field(name = "Rating",value = str(anime.rating))
        embed.add_field(name = "Broadcast",value = str(anime.broadcast))
        embed.add_field(name = "Status",value = str(anime.status))
        embed.add_field(name = "Type",value = str(anime.type))
        embed.add_field(name = "NSFW status",value = str(anime.is_nsfw()))
        embed.set_thumbnail(url = anime.poster)
        await ctx.send(embed = embed)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def animenews(self,ctx,amount:int=3):
        "Get updated with the latest news regarding Anime Industry."
        if amount>9:
            return await ctx.send("Please keep the amount less than 9 at a time to avoid spamming")
        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        descriptions = news.description
        
        embed = discord.Embed(title = "Latest Anime News",color = discord.Color.random(),timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url=news.images[0])

        for i in range(amount):
            embed.add_field(name = f"{i+1}) {titles[i]}", value = f"{descriptions[i][:200]}...\n[Read more]({links[i]})",inline=False)

        await ctx.send(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Anime(bot))
