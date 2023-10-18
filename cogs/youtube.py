import discord, requests, json
from config import *
from discord.ext import commands

REGIONS = """
AE : United Arab Emirates
BH : Bahrain
DZ : Algeria
EG : Egypt
IQ : Iraq
JO : Jordan
KW : Kuwait
LB : Lebanon
LY : Libya
MA : Morocco
OM : Oman
QA : Qatar
SA : Saudi Arabia
TN : Tunisia
YE : Yemen
AZ : Azerbaijan
BY : Belarus
BG : Bulgaria
BD : Bangladesh
BA : Bosnia and Herzegovina
CZ : Czechia
DK : Denmark
AT : Austria
CH : Switzerland
DE : Germany
GR : Greece
AU : Australia
BE : Belgium
CA : Canada
GB : United Kingdom
GH : Ghana
IE : Ireland
IL : Israel
IN : India
JM : Jamaica
KE : Kenya
MT : Malta
NG : Nigeria
NZ : New Zealand
SG : Singapore
UG : Uganda
US : United States
ZA : South Africa
ZW : Zimbabwe
AR : Argentina
BO : Bolivia
CL : Chile
CO : Colombia
CR : Costa Rica
DO : Dominican Republic
EC : Ecuador
ES : Spain
GT : Guatemala
HN : Honduras
MX : Mexico
NI : Nicaragua
PA : Panama
PE : Peru
PR : Puerto Rico
PY : Paraguay
SV : El Salvador
UY : Uruguay
VE : Venezuela
EE : Estonia
FI : Finland
PH : Philippines
FR : France
SN : Senegal
HR : Croatia
HU : Hungary
ID : Indonesia
IS : Iceland
IT : Italy
JP : Japan
GE : Georgia
KZ : Kazakhstan
KR : South Korea
LU : Luxembourg
LA : Laos
LT : Lithuania
LV : Latvia
MK : North Macedonia
MY : Malaysia
NO : Norway
NP : Nepal
NL : Netherlands
PL : Poland
BR : Brazil
PT : Portugal
RO : Romania
RU : Russia
LK : Sri Lanka
SK : Slovakia
SI : Slovenia
ME : Montenegro
RS : Serbia
SE : Sweden
TZ : Tanzania
TH : Thailand
TR : Turkey
UA : Ukraine
PK : Pakistan
VN : Vietnam
HK : Hong Kong
TW : Taiwan
CY : Cyprus
KH : Cambodia
LI : Liechtenstein
PG : Papua New Guinea
"""
async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Youtube(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(with_app_command=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def ytsearch(self, ctx, *, query:str):
        "Rich Youtube search command."
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&safeSearch=strict&type=video&key={API_KEY}"
        
        r = requests.get(url)
        data = json.loads(r.text)

        channel_data = r.json()["items"][0]["snippet"]
        video_id = r.json()["items"][0]["id"]["videoId"]
        channel_url=f"https://www.youtube.com/channel/{channel_data['channelId']}"
        video_url = f"https://www.youtube.com/watch?v={data['items'][0]['id']['videoId']}"
        
        url2 = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"

        r2 = requests.get(url2)
        data2 =json.loads(r2.text)

        with open("data.json", "w") as file:
            file.write(json.dumps(data2))

        video_data = r2.json()["items"][0]["statistics"]

        likes = video_data["likeCount"]
        views = video_data["viewCount"]

        embed = discord.Embed(title=channel_data["title"],url=video_url,description=channel_data["description"])
        embed.set_author(name=channel_data["channelTitle"],url=channel_url)
        embed.set_image(url=channel_data["thumbnails"]["medium"]["url"])
        embed.set_footer(text=f"Likes: {likes}, Views: {views}")

        await ctx.send(embed=embed)
    
    @commands.hybrid_command(with_app_command=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def ytchannel(self, ctx, *, query):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=channel&key={API_KEY}"
        
        r = requests.get(url)
        data = json.loads(r.text)

        channel_data = r.json()["items"][0]["snippet"]
        channel_id = r.json()["items"][0]["id"]["channelId"]
        channel_url=f"https://www.youtube.com/channel/{channel_data['channelId']}"
        
        url2 = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"

        r2 = requests.get(url2)
        data2 =json.loads(r2.text)

        with open("data.json", "w") as file:
            file.write(json.dumps(data2))

        embed = discord.Embed(title=channel_data["title"], url = channel_url, description=channel_data["description"])
        embed.set_thumbnail(url=channel_data["thumbnails"]["high"]["url"])

        await ctx.send(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def trending(self, ctx, region = None):
        if region == None:
            embed = discord.Embed(title="Regions Supported by YouTube", description=REGIONS, colour= discord.Color.random())
            return await ctx.send(embed=embed)

        trending_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode={region}&key={API_KEY}"
        response = requests.get(trending_url)
        data = json.loads(response.text)
        trending_videos = response.json()["items"]

        if len(trending_videos) == 0:
            return await ctx.send("Sorry, I couldn't find any trending videos in that region.")

        with open("data.json", "w") as file:
            file.write(json.dumps(data))

        embed = discord.Embed(title=f"Top 5 Trending Videos in {region.upper()}")
        for i, video in enumerate(trending_videos[:5]):
            video_title = video["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            embed.add_field(name=f"{i+1}. {video_title}", value=video_url,inline=False)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Youtube(bot))
