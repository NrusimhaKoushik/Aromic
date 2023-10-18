import animec
import discord
import datetime
from aiohttp import ClientSession
from discord.ext import commands

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Anime(commands.Cog):
    """Anime commmands for weebs"""
    def __init__(self,bot):
        self.bot = bot

    async def getWaifu(self, tag):
        async with ClientSession() as resp:
            async with resp.get(f'https://api.waifu.im/search/?included_tags={tag}') as response:
                data = await response.json()
        return data['images'][0]['url']

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

    # @commands.hybrid_command()
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def image(self,ctx,*,query):
    #     channel = self.bot.get_channel(1145264073865437194)
    #     """Search any anime Character"""
    #     try:
    #         char = animec.Charsearch(query)
    #     except Exception as e:
    #         await channel.send(f"```Error: {e}```")
    #         await ctx.send(embed=  discord.Embed(description = "No corresponding Anime Character is found for the search query",color = discord.Color.red()))
    #         return

    #     embed = discord.Embed(title = char.title,url = char.url,color = discord.Color.random())
    #     embed.set_image(url = char.image_url)
    #     embed.set_footer(text = ", ".join(list(char.references.keys())[:2]))
    #     await ctx.send(embed = embed)

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

    # @commands.command(name='uniform', description='Get waifu related to uniform!')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def uniform(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('uniform')))
    
    # @commands.command(name='maid', description='Get waifu related to maid')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def maid(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('maid')))
    
    # @commands.command(name='waifu', description='Get waifu related to waifu')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def waifu(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('waifu')))
    
    # @commands.command(name='marin-kitagawa', description='Get waifu related to marin-kitagawa')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def marin_kitagawa(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('marin-kitagawa')))
    
    # @commands.command(name='mori-calliope', description='Get waifu related to mori-calliope')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def mori_calliope(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('mori-calliope')))

    # @commands.command(name='raiden-shogun', description='Get waifu related to raiden-shogun')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def raiden_shogun(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('raiden-shogun')))

    # @commands.command(name='oppai', description='Get waifu related to oppai')
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def oppai(self, ctx):
    #     await ctx.send(embed=discord.Embed().set_image(url=await self.getWaifu('oppai')))

async def setup(bot: commands.Bot):
    await bot.add_cog(Anime(bot))