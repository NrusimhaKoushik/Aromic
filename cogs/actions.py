import discord
import random
import animec
from discord.ext import commands

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name ='pat',description='Get pat gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def pat(self, ctx, member: discord.Member):
        "Get patting GIFs"
        author = ctx.author.name
        mention = member.name
        
        pat = "{0} got patted by {1}!"
        
        # choices = ['https://media.giphy.com/media/lTyrzdLFF1ukiZ6NQc/giphy.gif',
        #            'https://media.giphy.com/media/nq9ALH4edwvFvwViXE/giphy.gif',
        #            'https://media.giphy.com/media/s4oNnqhd0ilYwHqwA4/giphy.gif',
        #            'https://media.giphy.com/media/0n8t38Jjd52Vn6yKeA/giphy.gif',
        #            'https://media.giphy.com/media/zYsmD2xOQh9VRzjZY2/giphy.gif',
        #            'https://media.giphy.com/media/H6gDspl0AS4nUX8XOl/giphy.gif',
        #            'https://media.giphy.com/media/Np6P4nNMWZAWbzUduZ/giphy.gif',
        #            'https://media.giphy.com/media/KvnZBsQJedmh814emA/giphy.gif',
        #            'https://media.giphy.com/media/yIGgrRpdZjuUBeFC2i/giphy.gif',
        #            'https://media.giphy.com/media/qx50Fo8OcyYhtsyQ3K/giphy.gif',
        #            'https://media.giphy.com/media/gSidK32fbCfVjCawlX/giphy.gif',
        #            'https://media.giphy.com/media/G9ukFCY101HCNbpF46/giphy.gif',
        #            'https://media.giphy.com/media/XycFhaROSN9M4aaEoo/giphy.gif',
        #            'https://media.giphy.com/media/IrQKeZM9MzV76K3C5x/giphy.gif',
        #            'https://media.giphy.com/media/21xepiGUks8N8EYOuK/giphy.gif',
        #            'https://media.giphy.com/media/Zj9YquiY6BK1fAHmWa/giphy.gif',
        #            'https://media.giphy.com/media/tQts45RbGhGLV8KSs7/giphy.gif',
        #            'https://media.giphy.com/media/HfriTla6D7gEn9zNkp/giphy.gif',
        #            'https://media.giphy.com/media/BuoGxgnfKYKpZ8o9RU/giphy.gif',
        #            'https://media.giphy.com/media/7mtYC8EfU5f7NWIyoA/giphy.gif',
        #            'https://media.giphy.com/media/vq3DVEEPCCNkgyxGqz/giphy.gif',
        #            'https://media.giphy.com/media/B4pLfbJxVSobgvbK6F/giphy.gif',
        #            'https://media.giphy.com/media/DiOUOiusECTDi0A7iT/giphy.gif',
        #            'https://media.giphy.com/media/I1BHAVI2xrsgRzKmpX/giphy.gif',
        #            'https://media.giphy.com/media/zsFp1U2lhhCy0tPlcN/giphy.gif',
        #            'https://media.giphy.com/media/6UflmA9OTHeUnLzLYP/giphy.gif',
        #            'https://media.giphy.com/media/3OiMVTCg6K8NLf66tu/giphy.gif',
        #            'https://media.giphy.com/media/eqkVxa7v420ipMHSCM/giphy.gif',
        #            'https://media.giphy.com/media/bMXsFTeMqyolbVLmEO/giphy.gif',
        #            'https://media.giphy.com/media/y3oBgEtNHG6YZGfLfJ/giphy.gif',
        #            'https://media.giphy.com/media/WVRIANaVxp3kQunqyq/giphy.gif',
        #            'https://media.giphy.com/media/Ivifi7dGFk6qxYBXQA/giphy.gif',
        #            'https://media.giphy.com/media/tnFRnRd1996qal9TsW/giphy.gif',
        #            'https://media.giphy.com/media/YqCMvs5QIKuBvhr4oz/giphy.gif',
        #            'https://media.giphy.com/media/SDzvXFpx4zC2z4JjRe/giphy.gif',
        #            'https://media.giphy.com/media/7FOgqdAQSYrRBG0DGf/giphy.gif',
        #            'https://media.giphy.com/media/qXyE1GCOelab1EHIQJ/giphy.gif',
        #            'https://media.giphy.com/media/Ti7bW8yNwIFtrucSmy/giphy.gif',
        #            'https://media.giphy.com/media/asymqFGmpXcH3Tq15H/giphy.gif',
        #            'https://media.giphy.com/media/7S6LJf5iqp1ZRkiN9b/giphy.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.pat()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=pat.format(mention, author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @pat.error
    async def pat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='kill',description='Get kill gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def kill(self, ctx, member: discord.Member):
        "Get killing GIFs"
        author = ctx.author.name
        mention = member.name
        
        kill = "{0} got killed by {1}!"
        
        # choices = ['https://media.giphy.com/media/HCOzoet1jc91AYKGcN/giphy.gif',
        #           'https://media.giphy.com/media/R4lxv1AB1KShQSAtPn/giphy.gif',
        #           'https://media.giphy.com/media/OvPtYRPCrvROVEAGws/giphy.gif',
        #           'https://media.giphy.com/media/zekUsVl0MymVhaaFoK/giphy.gif',
        #           'https://media.giphy.com/media/DekT1GkDGsmSaEVEAd/giphy.gif',
        #           'https://media.giphy.com/media/3svUxI7oKIYUHO5Eqv/giphy.gif',
        #           'https://media.giphy.com/media/OQoCKlfkYAMVdPJfLc/giphy.gif',
        #           'https://media.giphy.com/media/rTpLaQvDlNoKD5rdJQ/giphy.gif',
        #           'https://media.giphy.com/media/ZkOS6n8Zg3t98AmPBx/giphy.gif',
        #           'https://media.giphy.com/media/NGyQQTwcGhmp5xiOAE/giphy.gif',
        #           'https://media.giphy.com/media/LhLJcjihzNWZED1nJr/giphy.gif',
        #           'https://media.giphy.com/media/DRPnjGAb96e172NYZV/giphy.gif',
        #           'https://media.giphy.com/media/EjwT8rJOq6wBnuLdSb/giphy.gif',
        #           'https://media.giphy.com/media/Ez1exC7jjtKssT1Hr6/giphy.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.kill()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=kill.format(mention, author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='hug',description='Get hug gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def hug(self, ctx, member: discord.Member):
        "Get hugging GIFs"
        author = ctx.author.name
        mention = member.name
        
        hug = "{0} got hugged by {1}!"
        
        # choices = ['https://i.imgur.com/wOmoeF8.gif',
        #           'https://i.imgur.com/nrdYNtL.gif',
        #           'https://i.imgur.com/4oLIrwj.gif',
        #           'https://i.imgur.com/6qYOUQF.gif',
        #           'https://i.imgur.com/JiFpT5E.gif',
        #           'https://i.imgur.com/6PrF0xm.gif',
        #           'https://i.imgur.com/y1baEfE.gif',
        #           'https://i.imgur.com/UeuRbc6.gif',
        #           'https://i.imgur.com/CNq9Rt4.gif',
        #           "https://i.pinimg.com/originals/f2/80/5f/f2805f274471676c96aff2bc9fbedd70.gif",
        #           "https://i.pinimg.com/originals/85/72/a1/8572a1d1ebaa45fae290e6760b59caac.gif",
        #           "http://25.media.tumblr.com/tumblr_ma7l17EWnk1rq65rlo1_500.gif",
        #           "https://i.imgur.com/r9aU2xv.gif",
        #           "https://i.gifer.com/2QEa.gif",
        #           "https://25.media.tumblr.com/2a3ec53a742008eb61979af6b7148e8d/tumblr_mt1cllxlBr1s2tbc6o1_500.gif",
        #           "https://media3.giphy.com/media/sUIZWMnfd4Mb6/200.gif",
        #           "https://i.pinimg.com/originals/f9/e9/34/f9e934cddfd6fefe0079ab559ef32ab4.gif",
        #           "https://media3.giphy.com/media/wnsgren9NtITS/giphy.gif",
        #           "https://38.media.tumblr.com/b22e5793e257faf94cec24ba034d46cd/tumblr_nldku9v7ar1ttpgxko1_500.gif",
        #           "https://i.pinimg.com/originals/0c/bc/37/0cbc377124f2f91d76277160b5803372.gif",
        #           "https://78.media.tumblr.com/88b9b721e47c33272a3cafd0fdb916b5/tumblr_oqkfe3BbYM1vb10byo1_500.gif"
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.hug()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=hug.format(mention, author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='slap',description='Get slap gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def slap(self, ctx, member: discord.Member):
        "Get slapping GIFs"
        author = ctx.author.name
        mention = member.name
        
        slap = "{0} got slapped by {1}!"
        
        # choices = ['https://i.imgur.com/o2SJYUS.gif',
        #           'https://i.imgur.com/mIg8erJ.gif',
        #           'https://i.imgur.com/CwbYjBX.gif',
        #           'https://i.imgur.com/oRsaSyU.gif',
        #           'https://i.imgur.com/oOCq3Bt.gif',
        #           'https://i.imgur.com/fm49srQ.gif',
        #           'https://i.imgur.com/Li9mx3A.gif',
        #           'https://i.imgur.com/xxLRyua.gif',
        #           'https://i.imgur.com/HcTCdJ1.gif',
        #           'https://i.imgur.com/HcTCdJ1.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.slap()
        
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=slap.format(mention, author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='highfive',description='Get highfive gifs!', alises=['hf'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def highfive(self, ctx, member: discord.Member):
        "Get highfive GIFs"
        author = ctx.author.name
        mention = member.name
        
        punch = "{0} and {1} both did highfive!"
        
        # choices = ['https://i.imgur.com/g6cHmkQ.gif',
        #           'https://i.imgur.com/cWvWCKB.gif',
        #           'https://i.imgur.com/Rk6mdMO.gif',
        #           'https://i.imgur.com/H8npW4P.gif',
        #           'https://i.imgur.com/KExdGMd.gif',
        #           'https://i.imgur.com/6f8R8oy.gif',
        #           'https://i.imgur.com/P7HFmC3.gif',
        #           'https://i.imgur.com/gst0Xsv.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.highfive()
        
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=punch.format(mention, author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @highfive.error
    async def highfive_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='smile',description='Get smile gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def smile(self, ctx):
        "Get smiling GIFs"
        author = ctx.author.name
        
        smile = "{0} smiles! c:!"
        
        # choices = ['https://media.giphy.com/media/pNurrWijMObWP9cJKa/giphy.gif',
        #           'https://media.giphy.com/media/XwtxedEUHp7GxkVaOu/giphy.gif',
        #           'https://media.giphy.com/media/cKRYZ4YvbYweJYv5Sz/giphy.gif',
        #           'https://media.giphy.com/media/2PTOKQJIKiAJwLOzen/giphy.gif',
        #           'https://media.giphy.com/media/WtPoJWuCrOUney0BKI/giphy.gif',
        #           'https://media.giphy.com/media/n0U4yTCbb3HiyPwOI3/giphy.gif',
        #           'https://media.giphy.com/media/sXNY7Wh8drZpJPS6DO/giphy.gif',
        #           'https://media.giphy.com/media/0QkJx2dnIdjlYxGkUQ/giphy.gif',
        #           'https://media.giphy.com/media/kgc1q8FHJo8rhiTdhF/giphy.gif',
        #           'https://media.giphy.com/media/oi39yLqvmcQnPbC9dt/giphy.gif',
        #           'https://media.giphy.com/media/7cbgqigQWEX3sGz4VV/giphy.gif',
        #           'https://media.giphy.com/media/slUK70rmu3xAscOUXZ/giphy.gif',
        #           'https://media.giphy.com/media/PGvKy05bhJfKudALwr/giphy.gif',
        #           'https://media.giphy.com/media/J74U53PATIrngAzm1t/giphy.gif',
        #           'https://media.giphy.com/media/Mmp6UElGiebg4WoVFl/giphy.gif',
        #           'https://media.giphy.com/media/LTbztoE9YvXV0cg6P0/giphy.gif',
        #           'https://media.giphy.com/media/WexoPMOgMpUIAhUYqs/giphy.gif',
        #           'https://media.giphy.com/media/QWxrq7rsKim2BRHGRN/giphy.gif',
        #           'https://media.giphy.com/media/txjISyAv3bLzINrJwx/giphy.gif',
        #           'https://media.giphy.com/media/w0alAVkmLd1Yz3qw74/giphy.gif',
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.smile()
        
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=smile.format(author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @smile.error
    async def smile_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='cry',description='Get cry gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def cry(self, ctx):
        "Get crying GIFs"
        author = ctx.author.name
        
        sad = "{0} is sad,they need a hug!"
        
        # choices = ['https://media.giphy.com/media/2IlPXIpprK1dfyUN0a/giphy.gif',
        #           'https://media.giphy.com/media/LAAprQWylbAJbLV8r1/giphy.gif',
        #           'https://media.giphy.com/media/bB9hzRmw4p8B6Rra6s/giphy.gif',
        #           'https://media.giphy.com/media/buJH7JhmancEsEZXLn/giphy.gif',
        #           'https://media.giphy.com/media/Ig69sF3DJRxDnlsxBr/giphy.gif',
        #           'https://media.giphy.com/media/hEa9TXVYlnupS46Qt9/giphy.gif',   
        #           'https://media.giphy.com/media/w5oQ81UmFr0berjcEJ/giphy.gif',
        #           'https://media.giphy.com/media/mOMu7Mq6jgEmr5FZBd/giphy.gif',
        #           'https://media.giphy.com/media/yUl6BTa2TAnvcuLsqT/giphy.gif',
        #           'https://media.giphy.com/media/4eVwPyJfzN3c0Rss9c/giphy.gif',
        #           'https://media.giphy.com/media/P6fVByinx5oneOEzga/giphy.gif',
        #           'https://media.giphy.com/media/U9c3mZxdwzgusIhbjN/giphy.gif',
        #           'https://media.giphy.com/media/mS1ehaEs90WHhlLJxa/giphy.gif',
        #           'https://media.giphy.com/media/MJBPC1Gobdqo9destZ/giphy.gif',
        #           'https://media.giphy.com/media/H54pREoMFGFasne75t/giphy.gif',
        #           'https://media.giphy.com/media/nDnR25Kylc6TZPrGdI/giphy.gif',
        #           'https://media.giphy.com/media/61k5PsuGSdj7kAX63m/giphy.gif',
        #           'https://media.giphy.com/media/7ElzTGytX45kRPCxwt/giphy.gif',
        #           'https://media.giphy.com/media/KldRmWbXfSFIgJxV3z/giphy.gif',
        #           'https://media.giphy.com/media/Sm31qYSmoBlGh9jgHS/giphy.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.cry()
        
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=sad.format(author), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @cry.error
    async def cry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='forekiss',description='Get forekiss gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def forekiss(self, ctx, member: discord.Member):
        "Get forehead kissing GIFs"
        author = ctx.author.name
        mention = member.name
        
        forekiss = "{1} got a forehead kiss by {0}!"
        
        choices = ['https://media.giphy.com/media/Ga5bXXU5fFQ1XgzYke/giphy.gif',
                  'https://media.giphy.com/media/hJ7Qj0ccdu0ftp5nUZ/giphy.gif',
                  'https://media.giphy.com/media/KLhH38hdVqFPSGXLc0/giphy.gif',
                  'https://media.giphy.com/media/9fjMSkzqHurpsYyauF/giphy.gif',
                  'https://media.giphy.com/media/uBNLgPjrBdR0LAjY1T/giphy.gif',
                  'https://media.giphy.com/media/IHbNNT1ViZj2fZ5Wlh/giphy.gif',
                  'https://media.giphy.com/media/ICiF1vWfpRqAT4jz80/giphy.gif',
                  'https://media.giphy.com/media/tZlJ0j0tnGj8c1kasE/giphy.gif'
                  ]
        
        image = random.choice(choices)
        
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=forekiss.format(author, mention), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @forekiss.error
    async def forekiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)

    @commands.command(name ='kiss',description='Get kiss gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def kiss(self, ctx, member: discord.Member):
        "Get kissing GIFs"
        author = ctx.author.name
        mention = member.name
        
        forekiss = "{0} kissed {1}!"
        
        image = animec.Waifu.kiss()

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=forekiss.format(author, mention), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='spank',description='Get spank gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def spank(self, ctx, member: discord.Member):
        "Get spank GIFs"
        author = ctx.author.name
        mention = member.name
        
        spank = "{1} was spanked by {0}!"
        
        choices = ['https://media.giphy.com/media/uwYCUjtdEUJfr580Yq/giphy.gif',
                  'https://media.giphy.com/media/dyX4UOsHI9HfD4tZgl/giphy.gif',
                  'https://media.giphy.com/media/lNYNXjXl7wgMzPAyJ8/giphy.gif',
                  'https://media.giphy.com/media/f4xqH0wpAijyGxFpIt/giphy.gif',
                  'https://media.giphy.com/media/liOMwlRqFAcNkBNJr7/giphy.gif',
                  'https://media.giphy.com/media/8vGYTx47z5VLu6Sofa/giphy.gif',
                  'https://media.giphy.com/media/xEFLUoRqVKnkGKQLfC/giphy.gif',
                  'https://media.giphy.com/media/qPeVnT4JsgVVS3ySN9/giphy.gif'
                  ]
        
        image = random.choice(choices)
        
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=spank.format(author, mention), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @spank.error
    async def spank_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(description='Get kick gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def blow(self, ctx, member: discord.Member):
        "Get kicking GIFs"
        author = ctx.author.name
        mention = member.name
        
        blow = "{1} was kicked by {0}!"
        
        # choices = ['https://media.giphy.com/media/s8OP81wq8gqqWhcCDl/giphy.gif',
        #           'https://media.giphy.com/media/f0lE8PNcLnH7mR3Bz2/giphy.gif',
        #           'https://media.giphy.com/media/6apuBnrQEmzf6n5cnE/giphy.gif',
        #           'https://media.giphy.com/media/PwgNzvsZrzjRsqF4mf/giphy.gif',
        #           'https://media.giphy.com/media/KsbpFjh33kLL76pBOB/giphy.gif',
        #           'https://media.giphy.com/media/smRA1zfIWTndh6GQsk/giphy.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.kick()
        
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=blow.format(author, mention), url=image)
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    
    @blow.error
    async def blow_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='bully',description='Get bully gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def bully(self, ctx, member: discord.Member):
        "Get bullying GIFs"
        author = ctx.author.name
        mention = member.name
        
        bully = "{1} was bullied by {0}!"
        
        # choices = ['https://media.giphy.com/media/fXoiwS6AV8bTZxy4FL/giphy.gif',
        #           'https://media.giphy.com/media/sTB3RYdMbfyoWsoF3e/giphy.gif',
        #           'https://media.giphy.com/media/CcNu2fOFC4SZvZ11Th/giphy.gif',
        #           'https://media.giphy.com/media/vPHeH77uFJikmX5K55/giphy.gif',
        #           'https://media.giphy.com/media/jJaCARS3V3NxW4tfxu/giphy.gif',
        #           'https://media.giphy.com/media/Y01sK6clKzo5VW8Wh2/giphy.gif',
        #           'https://media.giphy.com/media/IF3Isn5LydbDdvErY8/giphy.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.bully()
        
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=bully.format(author, mention), url=image)
        embed.set_image(url=image)
 
        await ctx.send(embed=embed)
    
    @bully.error
    async def bully_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)
    
    @commands.command(name ='blush',description='Get blush gifs!')
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def blush(self, ctx):
        "Get blushing GIFs"
        author = ctx.author.name
        
        stare = "{0} blushed!"
        
        # choices = ['https://media.giphy.com/media/O8X1OjJTs9LFzpSMrS/giphy.gif',
        #           'https://media.giphy.com/media/rD9HDSUvqi1OLlqGiQ/giphy.gif',
        #           'https://media.giphy.com/media/ct4Pc9mGKS3JKvb0wP/giphy.gif',
        #           'https://media.giphy.com/media/oQkGNz9JvMu4RVRF6z/giphy.gif',
        #           'https://media.giphy.com/media/7wGUAdBMckSHvp18mM/giphy.gif'
        #           ]
        
        # image = random.choice(choices)
        image = animec.Waifu.blush()
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=stare.format(author), url=image)
        embed.set_image(url=image)
 
        await ctx.send(embed=embed)
     
    @blush.error
    async def stare_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 | Please tag someone!", delete_after = 2)

async def setup(bot: commands.Bot):
    await bot.add_cog(Actions(bot))