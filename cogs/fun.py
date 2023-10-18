import discord, aiohttp, requests, random, asyncio
from jokeapi import Jokes
from discord.ext import commands

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colour = [0x4555ff,0xffcc00,0x9d47ff,0xff47ff,0x47ff9a,0x47ffe6,0x47e3ff,0xffa647,0xff8a47,0xff4747,0x8147ff,0x4747ff]

    @commands.hybrid_command()
    async def joke(self, ctx: commands.Context):
        "Get random Jokes."
        j = await Jokes()
        blacklist = ["racist"]
        if not ctx.message.channel.is_nsfw():
            blacklist.append("nsfw")
        joke = await j.get_joke(blacklist=blacklist)
        msg = ""
        if joke["type"] == "single":
            msg = joke["joke"]
        else:
            msg = joke["setup"]
            msg += f"||{joke['delivery']}||"
        await ctx.send(msg)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def dog(self, ctx):
        "Random funny dog pics"
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://dog.ceo/api/breeds/image/random')
            dogjson = await request.json(content_type='application/json')
            # This time we'll get the fact request as well!
           # request2 = await session.get('https://some-random-api.ml/facts/dog')
            #factjson = await request2.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.blurple())
        embed.set_image(url=dogjson['message'])
        #embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def cat(self, ctx):
        "Random cute cat pics."
        async with aiohttp.ClientSession() as session:
            request = requests.get('http://thecatapi.com/api/images/get.php')
            #req = requests.get('http://catfacts-api.appspot.com/api/facts')
            if request.status_code == 200:
                image = request.url
            else:
                return await ctx.send("Error 404. API doesn't work well. A report was sent to the Developer to resolve the issue.")
            # if req.status_code = 200:
            #     fact = req.json()['facts'][0]
            # else:
            #     return await ctx.send('Error 404. Website may be down.')
            # This time we'll get the fact request as well!
            #request2 = await session.get('https://some-random-api.ml/facts/cat')
            #factjson = await request2.json()

        embed = discord.Embed(title="Meow!", color=discord.Color.blurple())
        embed.set_image(url=image)
        #embed.set_footer(text=fact)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        "Emojified text as you wish."
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {'0':'zero', '1':'one', '2':'two', '3':'three',
                        '4':'four', '5':'five', '6':'six', '7':'seven',
                        '8':'eight', '9':'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.send(''.join(emojis))

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please type something!", delete_after = 2)


    @commands.hybrid_command(pass_context=True)
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def meme(self, ctx):
        "Get random memes."
        embed = discord.Embed(title="", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def virus(self, ctx, user:commands.UserConverter = None, *, virus: str = "trojan"):
        "Inject Virus into someone you dont like."
        user = user or ctx.author
        if user.id == 853506728519532544:
            return await ctx.send(f'Can\'t inject virus into **{user.display_name}**.\nHe has advanced Virus protection. :shield:')
        list = (f"``[▓▓▓                    ] / {virus}-virus.exe Packing files.``",
                f"``[▓▓▓▓▓▓▓                ] - {virus}-virus.exe Packing files..``",
                f"``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {virus}-virus.exe Packing files..``",
                f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {virus}-virus.exe Packing files..``",
                f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {virus}-virus.exe Packing files..``",
                f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {virus}-virus.exe Packing files..``",
                f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {virus}-virus.exe Packing files..``",
                f"``Successfully downloaded {virus}-virus.exe``",
                "``Injecting virus.   |``",
                "``Injecting virus..  /``",
                "``Injecting virus... -``",
                f"``Successfully Injected {virus}-virus.exe into {user.name}``")
        for i in list:
            await asyncio.sleep(1)
            await ctx.send(content=i)

    @commands.hybrid_command(name="hack") #"Hacks" a tagged user or any phrase entered as argument
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hack(self,ctx, *, arg:commands.UserConverter=None):
        "Hack someone and get their information."
        if arg.id == 853506728519532544:
            return await ctx.send(f'Can\'t Hack **{arg.display_name}**.\nHe has advanced Hack protection. :shield:')
        
        balance=("$"+str(random.randint(1,9))+str(random.randint(1,9))+"."+str(random.randint(1,9))+str(random.randint(1,9)))
        msg = await ctx.send("Initiating hacking...")
        await asyncio.sleep(1)
        await msg.edit(content="Tracing IP address (0%)")
        await msg.edit(content="Tracing IP address (3%)")
        await asyncio.sleep(.5)
        await msg.edit(content="Tracing IP address (19%)")
        await msg.edit(content="Tracing IP address (30%)")
        await msg.edit(content="Tracing IP address (42%)")
        await asyncio.sleep(1)
        await msg.edit(content="Tracing IP address (56%)")
        await asyncio.sleep(2)
        await msg.edit(content="Tracing IP address (99%)")
        await msg.edit(content="**IP Trace Complete**\nIP: 506.457.14.512")
        await asyncio.sleep(1)
        await msg.edit(content="Accessing computer")
        await asyncio.sleep(.9)
        await msg.edit(content="Calculating possible passwords:\n`smalldick69`")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`los3rhed`")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`n0fri3nds123`")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`plsMarryMeS0meOne`")
        await msg.edit(content="Calculating possible passwords:\n`hahaXDlolLMAO`")
        await asyncio.sleep(1)
        await msg.edit(content="Accessed computer: Password = `password`")
        await msg.edit(content="Downloading trojan virus...")
        await asyncio.sleep(1)
        await msg.edit(content="Virus downloaded. Extracting information")
        await msg.edit(content="Email: `mikeOxsmall@yahoo.com`")
        await asyncio.sleep(1)
        await msg.edit(content="Latest Email: `RE: Confirmation of Donation to Erectile Dysfunction Charity`")
        await asyncio.sleep(2)
        await msg.edit(content="Sending resignation letter to boss")
        await asyncio.sleep(1)
        await msg.edit(content=f"Discord: {arg.mention}")
        await asyncio.sleep(1)
        await msg.edit(content="Current discord Status: `:heart_eyes: Simping for someone out of my league`")
        await asyncio.sleep(1)
        await msg.edit(content="Keylogging bank PIN... [--Loading--]")
        await asyncio.sleep(1)
        await msg.edit(content="Bank account retrieved\nCurrent Debit Card Balance: " + balance)
        await asyncio.sleep(1)
        await msg.edit(content="Tranferring balance to offshore account")
        await asyncio.sleep(.5)
        await msg.edit(content="Processing...")
        await asyncio.sleep(1)
        await msg.edit(content="Uninstalling Minecraft...")
        await asyncio.sleep(3)
        await msg.edit(content="Switching default browser to Internet Explorer")
        await asyncio.sleep(1)
        await msg.edit(content="Disabling adblocker")
        await asyncio.sleep(.9)
        await msg.edit(content="Medical records obtained")
        await asyncio.sleep(1)
        await msg.edit(content="Selling information to Government")
        await asyncio.sleep(2)
        await msg.edit(content="Hacking into school accounts...")
        await asyncio.sleep(1)
        await msg.edit(content="_Laughing at grades_")
        await asyncio.sleep(1)
        await msg.edit(content="Sending pics to teachers...[1/13]")
        await msg.edit(content="Sending pics to teachers...[3/13]")
        await msg.edit(content="Sending pics to teachers...[7/13]")
        await asyncio.sleep(2)
        await msg.edit(content="Sending pics to teachers...[10/13]")
        await asyncio.sleep(.9)
        await msg.edit(content="**ERROR** TEACHER SENT ONE BACK :flushed:")
        await asyncio.sleep(1)
        await msg.edit(content="Cannot compute... Cannot compute... Shutting down...")
        await asyncio.sleep(1)
        await msg.edit(content="*Initializing final completion procedures*")
        await asyncio.sleep(2)
        await msg.edit(content=(ctx.author.mention+", hack has been completed.\nComplete information here: <https://bit.ly/37cWufJ>"))
    
    @hack.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("We need a target!!! :rage: Our team of hackers are waiting! Use `^hack [user]`")

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))