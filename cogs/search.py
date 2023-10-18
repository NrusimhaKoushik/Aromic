import discord, requests, json, string, wikipedia
from discord.ext import commands
from config import *
from googletrans import Translator

LANGUAGES = """
'af': 'afrikaans'
'sq': 'albanian'
'am': 'amharic'
'ar': 'arabic'
'hy': 'armenian'
'az': 'azerbaijani'
'eu': 'basque'
'be': 'belarusian'
'bn': 'bengali'
'bs': 'bosnian'
'bg': 'bulgarian'
'ca': 'catalan'
'ceb': 'cebuano'
'ny': 'chichewa'
'zh-cn': 'chinese (simplified)'
'zh-tw': 'chinese (traditional)'
'co': 'corsican'
'hr': 'croatian'
'cs': 'czech'
'da': 'danish'
'nl': 'dutch'
'en': 'english'
'eo': 'esperanto'
'et': 'estonian'
'tl': 'filipino'
'fi': 'finnish'
'fr': 'french'
'fy': 'frisian'
'gl': 'galician'
'ka': 'georgian'
'de': 'german'
'el': 'greek'
'gu': 'gujarati'
'ht': 'haitian creole'
'ha': 'hausa'
'haw': 'hawaiian'
'iw': 'hebrew'
'he': 'hebrew'
'hi': 'hindi'
'hmn': 'hmong'
'hu': 'hungarian'
'is': 'icelandic'
'ig': 'igbo'
'id': 'indonesian'
'ga': 'irish'
'it': 'italian'
'ja': 'japanese'
'jw': 'javanese'
'kn': 'kannada'
'kk': 'kazakh'
'km': 'khmer'
'ko': 'korean'
'ku': 'kurdish (kurmanji)'
'ky': 'kyrgyz'
'lo': 'lao'
'la': 'latin'
'lv': 'latvian'
'lt': 'lithuanian'
'lb': 'luxembourgish'
'mk': 'macedonian'
'mg': 'malagasy'
'ms': 'malay'
'ml': 'malayalam'
'mt': 'maltese'
'mi': 'maori'
'mr': 'marathi'
'mn': 'mongolian'
'my': 'myanmar (burmese)'
'ne': 'nepali'
'no': 'norwegian'
'or': 'odia'
'ps': 'pashto'
'fa': 'persian'
'pl': 'polish'
'pt': 'portuguese'
'pa': 'punjabi'
'ro': 'romanian'
'ru': 'russian'
'sm': 'samoan'
'gd': 'scots gaelic'
'sr': 'serbian'
'st': 'sesotho'
'sn': 'shona'
'sd': 'sindhi'
'si': 'sinhala'
'sk': 'slovak'
'sl': 'slovenian'
'so': 'somali'
'es': 'spanish'
'su': 'sundanese'
'sw': 'swahili'
'sv': 'swedish'
'tg': 'tajik'
'ta': 'tamil'
'te': 'telugu'
'th': 'thai'
'tr': 'turkish'
'uk': 'ukrainian'
'ur': 'urdu'
'ug': 'uyghur'
'uz': 'uzbek'
'vi': 'vietnamese'
'cy': 'welsh'
'xh': 'xhosa'
'yi': 'yiddish'
'yo': 'yoruba'
'zu': 'zulu'
"""

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
            
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def googlesearch(self, ctx, *, query: str, count:int = None):
        "Search google and get what you searching for"
        if count <= 0:
            return await ctx.send(f"Maximum results should not be **{count}**.")
        if count == None:
            count = 1
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&num={count}"
        response = requests.get(url)
        results = json.loads(response.text)
        with open("data.json", "w") as file:
            file.write(json.dumps(results, indent=4, sort_keys=True))
        try:
            embed = discord.Embed(title="",description="", color = discord.Color.random())
            for i in results["items"]:
                title = i["title"]
                description = i["snippet"]
                link = i["link"]
                embed.add_field(name=f"**{title}**", value=f"{description}\n<{link}>", inline = False)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.send("No results found.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def imgsearch(self, ctx, *, query = None):
        "Get the query related Images."
        if query is None:
            query = 'random'
        try:
            url = f'https://api.unsplash.com/photos/random?page=1&query={query}&bot_id={IMAGE_ACCESS_KEY}'
            
            response = requests.get(url)
            data = response.json()
            
            image_url = data["urls"]["regular"]
            photographer_name = data["user"]["name"]
            photographer_url = data["user"]["portfolio_url"]
            photo = data['user']['profile_image']['medium']
            title = data["description"]

            if title is not None:
                if len(title) < 50:
                    embed = discord.Embed(title=f'{title}', url=image_url, color=discord.Color.random())
                elif len(title) > 50:
                    embed = discord.Embed(title=f'{title}', color=discord.Color.random())
            else:
                if query == 'random':
                    embed = discord.Embed(title=f'Random Image from the Internet', color=discord.Color.random())
                else:
                    embed = discord.Embed(title=f'Random {string.capwords(query)} Image', color=discord.Color.random())

            if photographer_url is not None:
                embed.set_author(name=f"Picture by {photographer_name}", icon_url=photo, url=photographer_url)
            else:
                embed.set_author(name=f"Picture by {photographer_name}")

            embed.set_image(url=image_url)
            embed.set_footer(text='Note: Some images are not accurate with the query.')

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.hybrid_command(aliases=['wikipedia'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def wiki(self, ctx, *, query):
        """Search for a Wikipedia article."""
        em = discord.Embed(title=str(query))
        em.set_footer(text='Powered by wikipedia.org')
        try:
            result = wikipedia.summary(query)
            if len(result) > 2000:
                em.color = discord.Color.red()
                em.description = f"Result is too long. View the website [here](https://wikipedia.org/wiki/{query.replace(' ', '_')}), or just google the subject."
                return await ctx.send(embed=em)
            em.color = discord.Color.green()
            em.description = result
            await ctx.send(embed=em)
        except wikipedia.exceptions.DisambiguationError as e:
            em.color = discord.Color.red()
            options = '\n'.join(e.options)
            em.description = f"**Options:**\n\n{options}"
            await ctx.send(embed=em)
        except wikipedia.exceptions.PageError:
            em.color = discord.Color.red()
            em.description = 'Error: Page not found.'
            await ctx.send(embed=em)
    
    @commands.hybrid_command(name ='lang',description='Translate words to specific Language',aliases = ['translate'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def translate(self, ctx, lang_to = None, *, arg = None):
        if lang_to is None:
            embed = discord.Embed(title='All Supported Language Codes', description=LANGUAGES, color=discord.Color.random())
            return await ctx.send(embed=embed)
        if arg is None:
            return await ctx.send('Hey gimme some text to translate next time!')
        trans = Translator()
        trs = trans.translate(arg, dest=lang_to)
        detected = trans.detect(arg)
        embed2 = discord.Embed(title = "Here is your translated text", description = f"`{trs.text}`", color = discord.Color.random())
        embed2.set_footer(text = f"Translated from {detected.lang} to {lang_to}.")
        await ctx.send(embed = embed2)

async def setup(bot: commands.Bot):
    await bot.add_cog(Search(bot))
