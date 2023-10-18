import discord, random, asyncio, aiosqlite
from PIL import ImageChops, Image, ImageFont, ImageDraw
from io import BytesIO
from mongo import db
from discord import Embed
from discord.ext import commands

words = ['conversation', 'bowtie', 'skateboard', 'penguin', 'hospital', 'player', 'kangaroo', 
		'garbage', 'whisper', 'achievement', 'flamingo', 'calculator', 'offense', 'spring', 
		'performance', 'sunburn', 'reverse', 'round', 'horse', 'nightmare', 'popcorn', 
		'hockey', 'exercise', 'programming', 'platypus', 'blading', 'music', 'opponent', 
		'electricity', 'telephone', 'scissors', 'pressure', 'monkey', 'coconut', 'backbone', 
		'rainbow', 'frequency', 'factory', 'cholesterol', 'lighthouse', 'president', 'palace', 
		'excellent', 'telescope', 'python', 'government', 'pineapple', 'volcano', 'alcohol', 
		'mailman', 'nature', 'dashboard', 'science', 'computer', 'circus', 'earthquake', 'bathroom', 
		'toast', 'football', 'cowboy', 'mattress', 'translate', 'entertainment', 'glasses', 
		'download', 'water', 'violence', 'whistle', 'alligator', 'independence', 'pizza', 
		'permission', 'board', 'pirate', 'battery', 'outside', 'condition', 'shallow', 'baseball', 
		'lightsaber', 'dentist', 'pinwheel', 'snowflake', 'stomach', 'reference', 'password', 'strength', 
		'mushroom', 'student', 'mathematics', 'instruction', 'newspaper', 'gingerbread', 
		'emergency', 'lawnmower', 'industry', 'evidence', 'dominoes', 'lightbulb', 'stingray', 
		'background', 'atmosphere', 'treasure', 'mosquito', 'popsicle', 'aircraft', 'photograph', 
		'imagination', 'landscape', 'digital', 'pepper', 'roller', 'bicycle', 'toothbrush', 'newsletter']  

images =   ['```\n   +---+\n   O   | \n  /|\\  | \n  / \\  | \n      ===```',   
			'```\n   +---+ \n   O   | \n  /|\\  | \n  /    | \n      ===```', 
			'```\n   +---+ \n   O   | \n  /|\\  | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n  /|   | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n   |   | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n       | \n       | \n      ===```', 
			'```\n  +---+ \n      | \n      | \n      | \n     ===```']

ship_board = ["```  A B C D E F G H\n1| | | | | | | | |\n2| | | | | | | | |\n3| | | | | | | | |\n4| | | | | | | | |\n5| | | | | | | | |\n6| | | | | | | | |\n7| | | | | | | | |\n8| | | | | | | | |```"]

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def findimposter(self, ctx):
        "Try to find the IMPOSTER..."
        embed1 = discord.Embed(title = "Who's the imposter?" , description = "Find out who the imposter is, before the reactor breaks down!" , color=0xff0000)
        
        embed1.add_field(name = 'Red' , value= '<:Red_Crewmate:916237299216437258>', inline=False)
        embed1.add_field(name = 'Blue' , value= '<:Blue_Crewmate:916237099957616671>', inline=False)
        embed1.add_field(name = 'Lime' , value= '<:Lime_Crewmate:916237121369546783>', inline=False)
        embed1.add_field(name = 'White' , value= '<:White_Crewmate:916237354296049685>', inline=False)
        
        msg = await ctx.send(embed=embed1)
        
        emojis = {
            'red': '<:Red_Crewmate:916237299216437258>',
            'blue': '<:Blue_Crewmate:916237099957616671>',
            'lime': '<:Lime_Crewmate:916237121369546783>',
            'white': '<:White_Crewmate:916237354296049685>'
        }
        
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]
        
        for emoji in emojis.values():
            await msg.add_reaction(emoji)
        
        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji) in emojis.values()

        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        except asyncio.TimeoutError:
            description = "Reactor Meltdown. **{0}** was the imposter...".format(imposter)
            embed = Embed(title="Defeat", description=description, color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if str(self.reacted) == emojis[imposter]:
                steal=['GG! Wait did you just stole 1000 coins from imposter?',
                    ':tada: You win. For your kind help, crewmates gave u 1000 coins. Lets gooo..',
                    'The Airship Pilot offers you a reward of 1000 coins. What you do with them? :thinking:',
                    'GG! You are rewarded with 1000 coins for saving the spaceship.',
                    'Imposter kicked out from the spaceship. GG! You got a reward 1000 coins.'
                    ]

                win_quote = random.choice(steal)
                description = f"**{imposter}** was the imposter...\n{win_quote}"
		
                embed = discord.Embed(title= f"Victory 🏆", description = description, color = discord.Color.green())
                await ctx.send(embed=embed)

            else:
                for key, value in emojis.items(): 
                    if value == str(self.reacted):
                        description = "**{0}** was not the imposter...\n Sorry you didnt get any coins. Enjoy your Defeat.".format(key)
                        embed = Embed(title="Defeat ❌", description=description, color=discord.Color.red())
                        await ctx.send(embed=embed)
                        break

    @commands.hybrid_command(name="rps", aliases=["rockpaperscissors"])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rps(self, ctx):
        "Can you win Rock Paper Scissors aganist me?"
        rpsEmojis=["🪨", "📄", "✂️"]
        
        embed=Embed(title=("So... you want to challenge me to rock paper scissors, huh?\nReact to this message with your choice"))
        botMsg = await ctx.send(embed=embed)
        
        for emoji in rpsEmojis:
            await botMsg.add_reaction(emoji)
        
        bChoice=random.choice(rpsEmojis)
        
        def rpsaction(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) in rpsEmojis))            
        
        try:
            response,_ = await self.bot.wait_for("reaction_add",check=rpsaction,timeout=30)

            if response.emoji==bChoice:
                resultsMsg=("We tied! You got super lucky...:expressionless:")

            elif response.emoji=="🌑":

                if bChoice=="📄":
                    resultsMsg=("LLLLL I chose paper, imagine losing :rofl:")

                else:
                    resultsMsg=("Oh... I chose scissors :fearful: You win I guess and won 50 coins.")

            elif response.emoji=="📄":

                if bChoice=="🌑":
                    resultsMsg=("Oh... I chose rock :fearful: You win I guess and won 50 coins.")

                else:
                    resultsMsg=("LLLLL I chose scissors, imagine losing :rofl:")

            else:

                if bChoice=="🌑":
                    resultsMsg=("LLLLL I chose rock, imagine losing :rofl:")

                else:
                    resultsMsg=("Oh... I chose paper :fearful: You win I guess and won 50 coins.")
            embed=Embed(title=resultsMsg)
            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            return await ctx.send("Thanks for taking so long, dipshit. I'm taking this as a win for me LLL")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(2, 120, commands.BucketType.user)
    async def hangman(self, ctx):
      "Try to find the word within the man hanged himself."
      def check(m):
        return m.author == ctx.author
      guesses = '' 
      turns = 6
      word = random.choice(words) 
      await ctx.send("Guess the characters:")
      guess_msg = await ctx.send(images[turns])
      word_msg = await ctx.send(f"`{' '.join('_'*len(word))}`")
      while turns > 0: 
        out = ''
        rem_chars = 0
        for char in word:  
          if char in guesses:  
            out += char
          else:  
            out += '_'
            rem_chars += 1
        await word_msg.edit(content=f"`{' '.join(out)}`")
        
        if rem_chars == 0: 
          await word_msg.edit(content=f'**{word}**')
          return await ctx.send("You Win 🏆.")

        try:
          msg = await self.bot.wait_for('message', check=check, timeout=20.0)
          if msg.content == 'exit':
            await ctx.send("You quit and ran away.")
            return
        except asyncio.TimeoutError:
          await ctx.send(f"You took too long {ctx.author.name} :hourglass:")
          await guess_msg.delete()
          await word_msg.delete()
          return

        guess =  msg.content[0]
        guesses += guess  
        await msg.delete()

        if guess not in word: 
          turns -= 1
          await ctx.send("Wrong :x:", delete_after=1.0) 
          await guess_msg.edit(content=images[turns])
          if turns == 0:
            await word_msg.edit(content=f'**{word}**')
            return await ctx.send(f"You Loose **{ctx.author.name}** :x:")

    @commands.hybrid_command(aliases=['tictactoe'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def ttt(self, ctx, member:discord.Member):
        "Play TicTacToe with friends."
        isFinished = False
        cr_player = member
        opp = member
        winner = None
        player = ctx.author
        #list of combinations
        combinations = [['1','2','3'],['4','5','6'],['7','8','9'],['1','4','7'],['2','5','8'],['3','6','9'],['1','5','9'],['3','5','7']]
        cr = '❌'
        cl = '⭕'
        bl = '⬛'
        tdict = {'1':bl,'2':bl,'3':bl,'4':bl,'5':bl,'6':bl,'7':bl,'8':bl,'9':bl}
        tlist = ['1','2','3','4','5','6','7','8','9']
        tttstr = ''
        for item in tlist:
            tttstr += tdict[item]
            if (tlist.index(item)+1) % 3 == 0:
                tttstr += '\n'
        #embed formation
        embed = discord.Embed(title=f'TicTacToe | {player.name} vs {opp.name}',color=discord.Color.orange())
        embed.add_field(name='How to play?',value='The game works on a grid system. For example "1" for the \ntop left corner and "9" for the bottom right corner.')
        emb = await ctx.send(embed=embed)
        board = await ctx.send(tttstr)
        while isFinished == False:
            
            if cr_player == member:
                def check(m):
                    return m.author == member and m.channel == ctx.channel
            else:
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
            await ctx.send(f'{cr_player.mention}, enter your square below!')
            msg2 = ''
            while msg2 not in tdict:
                msg = await self.bot.wait_for('message',check=check)
                msg2 = msg.content
            if msg.content.lower() == 'cancel':
                canbed = discord.Embed(title='Canceled',description=f'{cr_player.name} canceled the game :(',color=discord.Color.red())
                await ctx.send(embed=canbed)
                return
            
            if msg2 not in tdict:
                em2 = discord.Embed(title='Error',description='Please enter a valid square/coordinate!',color=discord.Color.red())
                await ctx.send(embed=em2)
            if msg.content.lower() == 'cancel':
                canbed = discord.Embed(title='Canceled',description=f'{cr_player.name} canceled the game :(',color=discord.Color.red())
                await ctx.send(embed=canbed)
                return
            sq = msg.content.lower()
            if tdict[sq] == bl:
                if cr_player == member:
                    tdict[sq] = cr
                else:
                    tdict[sq] = cl
            tttstr = ''
            for item in tlist:
                tttstr += tdict[item]
                if (tlist.index(item)+1) % 3 == 0:
                    tttstr += '\n'
            embed = discord.Embed(title=f'TicTacToe | {player.name} vs {opp.name}',color=discord.Color.orange())
            embed.set_footer(text='The game works on a grid system. For example "1" for the \ntop left corner and "9" for the bottom right corner.')
            await emb.edit(embed=embed)
            await ctx.send(tttstr)
            for item in combinations:
                if (tdict[item[0]] == cl and tdict[item[1]] == cl and tdict[item[2]] == cl) or (tdict[item[0]] == cr and tdict[item[1]] == cr and tdict[item[2]] == cr):
                    isFinished = True
                    winner = cr_player
                    break
                allFilled = False
                if bl not in list(tdict.values()):
                    allFilled = True
                    isFinished = True
                    break
            if cr_player == member:
                cr_player = player 
            else:
                cr_player = member
        if winner == None:
            em2 = discord.Embed(title='No one won :(',description='No one won the tictactoe game!',color=discord.Color.red())
        else:
            em2 = discord.Embed(title='Winner!',description=f'{winner.mention} won the tictactoe game!',color=discord.Color.green())
        await ctx.send(embed=em2)

    @ttt.error
    async def ttt_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a member to play this game.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players.")


    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.is_owner()
    async def battleship(self, ctx):
        Hidden_Pattern=[[' ']*8 for x in range(8)]
        Guess_Pattern=[[' ']*8 for x in range(8)]

        let_to_num={'A':0,'B':1, 'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

        await ctx.send(ship_board[0])
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot)) 
