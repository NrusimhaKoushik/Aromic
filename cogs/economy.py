import discord, asyncio, random, string , requests, json
from discord.ext import commands
from discord import app_commands,Interaction
from mongo import db
from config import *

password = ''.join(random.choice(string.ascii_letters) for i in range(10))
default = password
uniq_pass = random.randint(100000, 999999)

async def record_usage(self, ctx):
    channel_id = 1154133781758881874
    # Getting the channel
    channel = self.bot.get_channel(channel_id)
    embed = discord.Embed(title = 'Command Usage', description = f'**{ctx.author}** used `^{ctx.command}` at `{ctx.guild.name}`', color=ctx.author.color)
    await channel.send(embed=embed)

async def getprefix(bot, message):
    s = db.mycoll.find_one({"_id": message.guild.id})
    if s is not None:
        return s["prefix"]
    else:
        db.guild.insert_one({
            "_id": message.guild.id,
            "prefix": "^"
            })
        return "^"

def topgg_votecheck(user):
    url = f"https://top.gg/api/bots/1055437102042599445/check?userId={user.id}"
    r = requests.get(url)
    data = json.loads(r.text)
    print(data)
    try:
        if data["voted"] == 1:
            return True
        else:
            return False
    except KeyError:
        return "error"

def dbl_votecheck(user):
    headers = {'Authorization': DISCORD_BOT_LIST_TOKEN}
    response = requests.get(f'https://discordbotlist.com/api/v1/bots/1055437102042599445/upvotes', headers=headers)
    try:
        if response.status_code == 200:
            votes = response.json().get('upvotes')

        for i in votes:
            if i['user_id'] == user.id:
                return True
            else:
                return False
    except KeyError:
        return "error"

class CreateModal(discord.ui.Modal, title="Submit your credentials for Apay"):
    pwd = discord.ui.TextInput(style = discord.TextStyle.short, label = "Password", placeholder="Enter a new password for your Apay account")
    activity = discord.ui.TextInput(style = discord.TextStyle.short, label = "Rob Activities", placeholder = "Type Enable (or) Disable")

    async def on_submit(self, interaction: discord.Interaction):
        pwd = self.pwd.value
        activity = self.activity.value
        db.mycol.update_one({"_id":interaction.user.id}, {"$set":{"password":pwd}})
        if activity.lower() == "enable":
            db.mycol.update_one({"_id":interaction.user.id}, {"$set":{"rob_activity": "true"}})
            await interaction.response.send_message("Your account has been created.", ephemeral=True)
        elif activity.lower() == "disable":
            db.mycol.update_one({"_id":interaction.user.id}, {"$set":{"rob_activity": "false"}})
            await interaction.response.send_message("Your account has been created.", ephemeral=True)
        else:
            db.mycol.update_one({"_id":interaction.user.id}, {"$set":{"rob_activity": "true"}})
            await interaction.response.send_message("Wrong input for Rob Activities and enabled by default.\nYour account has been created.", ephemeral=True)
        
        find = db.mycol.find_one({"_id":interaction.user.id})
        name = interaction.user.name
        p = find["password"]
        wallet = find["wallet"]
        bank = find["bank"]
        maxbank = find["maxbank"]
        transactions = find["description"]
        uniq = find["unique_id"]

        if transactions == []:
            transactions = "No Transactions done."
        embed = discord.Embed(title=f"{name}'s Account Info", color = discord.Color.random())
        embed.add_field(name='Wallet', value=wallet)
        embed.add_field(name='Bank',value=f'{bank}/{maxbank}')
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name='Transactions', value=f'{transactions}')
        embed.add_field(name='Password', value=f'{p}')
        embed.add_field(name='Unique ID', value=f'{uniq}')
        embed.set_footer(text='⚠️ Note: Please keep safe your UniqueID and Password for future references.')
        return await interaction.user.send(embed=embed)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db

    async def create_account(self, id):
        self.db.mycol.insert_one({
            "_id": id,
            "wallet": 100,
            "bank": 0,
            "maxbank": 1000,
            "password": default,
            "description": [],
            "unique_id": uniq_pass,
            "daily": 86400,
            "daily_start": "no",
            "weekly": 604800,
            "weekly_start": "no",
            "monthly": 2628000,
            "monthly_start": "no",
            "rob_activity": "true",
            "in_jail": "no"
        })
    
    async def create_shop(self, name:str, id:str, desc:str, cost:int , items):
        self.db.shop.insert_one({
            "_id": id,
            "name": name,
            "desc": desc,
            "cost": cost,
            "items": items,
            "max_items": items
        })
    
    async def create_inv(self,user:discord.member):
        self.db.inventory.insert_one({
            "_id":user.id
        })
    
    @commands.Cog.listener()
    async def on_ready(self):
        for x in self.db.mycol.find():
            streak = x["daily_start"]
            if x:
                if streak == "yes":
                    self.db.mycol.update_many({"daily_start" : "yes"}, {"$set": {"daily_start" : "no"}})
                    print("Daily Start Updated!!")
                else:
                    pass

    @app_commands.command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def create(self, interaction: Interaction):
        """Create account for economy system."""
        # user = interaction.user.id
        # guild = interaction.guild.id
        # me = ctx.me
        # overwrites = {
        #     guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        #     user: discord.PermissionOverwrite(read_messages=True, send_messages= True),
        #     me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        # }

        c =  self.db.mycol.find_one({"_id":interaction.user.id})
        
        if c is None:
            await self.create_account(interaction.user.id)
            # await self.create_inv(ctx.author)
            modal = CreateModal()
            modal.user = interaction.user
            await interaction.response.send_modal(CreateModal())
        if c:
            return await interaction.response.send_message(f"You are already have account for Economy.")
                
    @commands.hybrid_command(aliases=['delacc'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def delete(self, ctx):
        "Delete your Economy profile."
        find = self.db.mycol.find_one({"_id":ctx.author.id})
        if find is not None:
            self.db.mycol.delete_one({"_id":ctx.author.id})
            self.db.inventory.delete_one({"_id":ctx.author.id})
            await ctx.send("Account was permanently deleted!! If you want to create again use `^create` to create a new account for you.")
        else:
            await ctx.send("You do not have an account. Use `^create` to create a new account for you.`")

    @commands.hybrid_command(aliases=["bal", "money"])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def balance(self, ctx, user: discord.Member=None):
        "Shows your economy balance"
        if user is None:
            user = ctx.author

        find = self.db.mycol.find_one({"_id":user.id})

        if find is None:
            await ctx.send("You don't have a account. Please use `^create` to create an account!")
            return
        
        wallet = find["wallet"]
        bank = find["bank"]
        maxbank = find["maxbank"]

        if user == ctx.author:
            em=discord.Embed(color=discord.Color.random())
            em.add_field(name='Wallet', value=wallet)
            em.add_field(name='Bank',value=f'{bank}/{maxbank}')
            em.set_author(name='Your Balance')
            em.set_thumbnail(url=user.display_avatar.url)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(color=discord.Color.random())
            em.add_field(name='Wallet', value=wallet)
            em.add_field(name='Bank',value=f'{bank}/{maxbank}')
            em.set_author(name=f'{user.name}\'s Balance')
            em.set_thumbnail(url=user.display_avatar.url)
            await ctx.send(embed=em)
    
    @commands.hybrid_command(aliases=['dep'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def deposit(self, ctx, *, amount = None):
        "Deposit money to economy account"
        user = ctx.author

        find = self.db.mycol.find_one({"_id":user.id})

        if find is None:
            await ctx.send("You don't have a account. Please use `^create` to create an account!")
            return
        
        if amount == None:
            return await ctx.send('-_- What should I deposit into bank your soul or amount? Please type amount next time!!')
        
        wallet = find['wallet']
        bank = find['bank']
        maxbank = find['maxbank']

        if amount.lower() == 'max' or amount.lower() == 'all':
            limit = maxbank - bank
            amount = wallet
            if amount > maxbank:
                amount = maxbank
            if amount > limit:
                amount = limit
        else:
            amount = int(amount)

        transactions = f'{amount} coins has debited to bank.'
        limit = maxbank - bank

        if wallet == 0:
            return await ctx.send('You do not have enough coins to Deposit.')
        if bank == maxbank:
            return await ctx.send("Bank was full can't deposit the money.")
        if amount < 0:
            return await ctx.send("Amount should not be less than 0.")
        if amount > wallet:
            return await ctx.send(f'You do not have **{amount}** coins in your wallet.')
        if amount > maxbank:
            return await ctx.send(f'Your bank limit is `{maxbank}`. You cannot deposit more than that.')
        if amount > limit:
            return await ctx.send(f"You can deposit {limit} amount in your bank.")
        
        updated_wallet = wallet - amount
        updated_bank = bank + amount
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"bank": updated_bank}})
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": updated_wallet}})
        self.db.mycol.update_one({"_id": user.id}, {"$push": {"description": transactions}})

        await ctx.send(f"{amount} coins has been debited from Wallet to your Bank.")

    @commands.hybrid_command(aliases=['with', 'wd'])
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def withdraw(self, ctx, *, amount = None):
        "Withdraw money from your economy account"
        user = ctx.author

        find = self.db.mycol.find_one({"_id":user.id})
        if find is None:
            return await ctx.send("You don't have a account. Please use `^create` to create an account!")
        
        if amount == None:
            return await ctx.send('-_- What should I withdraw into wallet coins or your soul? Please type amount next time!!')
        
        wallet = find['wallet']
        bank = find['bank']
        maxbank = find['maxbank']

        if amount.lower() == 'max' or amount.lower() == 'all':
            amount = bank
        else:
            amount = int(amount)

        transactions = f'{amount} coins has credited to wallet.'

        if bank == 0:
            return await ctx.send('You do not have enough coins to withdraw.')
        if amount > bank:
            return await ctx.send(f'You do not have **{amount}** coins in your wallet.')
        if amount < 0:
            return await ctx.send("Amount should not be less than 0.")

        updated_wallet = wallet + amount
        updated_bank = bank - amount
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"bank": updated_bank}})
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": updated_wallet}})
        self.db.mycol.update_one({"_id": user.id}, {"$push": {"description": transactions}})

        await ctx.send(f"{amount} coins has been credited from your Bank to Wallet.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        "Beg for coins"
        user = ctx.author
        chances = random.randint(1, 4)

        if chances == 1:
            return await ctx.send("You got Nothing. ")
        
        amount = random.randint(1, 2500)

        res = self.db.mycol.find_one({"_id":user.id})
        if res is None:
            return await ctx.send("You don't have a account. Please use `^create` to create an account!")
        
        wallet = res['wallet']

        updated_wallet = wallet + amount
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": updated_wallet}})

        if amount == 0:
            await ctx.send(f"How unlucky... You didn't get anything...")

        elif amount > 50:
            await ctx.send(f"Nice you got ${amount} from a cool dude")

        elif amount > 100:
            await ctx.send(f"Someone felt nice and gave you ${amount}")

        elif amount > 500:
            await ctx.send(f"You seem to have a way with people! Someone gave you ${amount}")

        elif amount > 800:
            await ctx.send(f"What a lucky day!! Someone gave you ${amount}")

        elif amount > 1500:
            await ctx.send(f"A rich man passed by you and felt bad. So ha gave you ${amount}")

        elif amount > 2000:
            await ctx.send(f"A shady man walked up to you and said 'I know how tough it can be out here' before giving you ${amount}")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def give(self, ctx, user:discord.Member = None, amount = None):
        "Give random amount of coins to your favourite person"
        amount = int(amount)
        if user is None:
            return await ctx.send("Mention a user to whom you want to give coins next time..")
        if amount is None:
            return await ctx.send("Mention amount to transfer.")
        if amount < 0:
            return await ctx.send("Amount should not be less than 0.")
        
        find = self.db.mycol.find_one({"_id": ctx.author.id})
        
        if find is None:
            return await ctx.send("You don't have an account. Please use `^create` to create an account!")
        
        find2 = self.db.mycol.find_one({"_id": user.id})

        if find2 is None:
            return await ctx.send(f"**{user.name}** don't have an account.")
        
        wallet = find["wallet"]
        wallet2 = find2["wallet"]

        if amount > wallet:
            return await ctx.send("You don't have enough coins to give.")
        
        self.db.mycol.update_one({"_id": ctx.author.id}, {"$set": {"wallet": wallet - amount}})
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": wallet2 + amount}})

        await ctx.send(f"**{amount}** coin(s) has been given to **{user.name}**.")

        em = discord.Embed(title='',description=f'**{ctx.author}** has send you **{amount}** coin(s), added to your wallet. Dont forget to Thank him.', color=discord.Color.random())
        await user.send(embed=em)

        # em2=discord.Embed(title='',description=f"You sent **{user}** **{amount}** coin(s) from your wallet. Lucky him to have a friend like you!!",color=discord.Color.random())
        # await ctx.author.send(embed=em2)

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def rob(self, ctx, user:discord.Member = None):
        "Rob someone and get their money!"
        if user is None:
            return await ctx.send("Wanna rob a ghost? Mention someone to rob dumb..")
        
        find = self.db.mycol.find_one({"_id": ctx.author.id})
        find2 = self.db.mycol.find_one({"_id":user.id})

        wallet = find["wallet"]
        wallet2 = find2["wallet"]

        if find is None:
            return await ctx.send("You don't have an account. Please use `^create` to create an account!")
        if find2 is None:
            return await ctx.send("User don't have an account to rob.")
        try:
            find_rob_activity = find["rob_activity"]
            find_in_jail = find["in_jail"]

            if find_rob_activity == "false":
                return await ctx.send(f"You can't rob **{ctx.author.display_name}**.\n`rob-activites = True`")
            if find_in_jail == "yes":
                return await ctx.send(f"You were in JAIL. How the hell gonna rob?")
            try:
                find2_rob_activity = find2["rob_activity"]
                find2_in_jail = find2["in_jail"]

                if find2_rob_activity == "false":
                    return await ctx.send(f"You can't rob **{user.display_name}**. User disabled the Rob Activities.")
                if find2_in_jail == "yes":
                    return await ctx.send(f"You were in JAIL. How the hell gonna rob?")
                
                choice = random.randint(0, 5)
                if choice == 0 or choice == 1:
                    if wallet < 50:
                        self.db.mycol.update_one({"_id":ctx.author.id}, {"$set":{"in_jail": "yes"}})
                        await ctx.send(f"You went to JAIL for tried to rob **{user.display_name}** in this poor condition.")
                        rand = random.randint(0, 86400)
                        await asyncio.sleep(rand)
                        self.db.mycol.update_one({"_id":ctx.author.id}, {"$set":{"in_jail": "no"}})

                    update_wallet = wallet * (90/100)
                    self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": wallet2 + int(update_wallet)}})
                    self.db.mycol.update_one({"_id": ctx.author.id}, {"$set": {"wallet": wallet - int(update_wallet)}})
                    return await ctx.send(f"You were CAUGHT **HAHAHA**.\nYou paid **{user.display_name}** - **{int(update_wallet)}** coins.")
                else:
                    if wallet2 < 50:
                        return await ctx.send(f"You just run away after seeing **{user.display_name}**'s poor condition.")
                    update_wallet = wallet2 * (95/100)
                    embed = discord.Embed(title=f'{user.display_name} got robbed by {ctx.author.display_name}',
                                          description=f"You somehow stole **{int(update_wallet)}** coins from {user.display_name}."
                                          )
                    self.db.mycol.update_one({"_id": ctx.author.id}, {"$set": {"wallet": wallet + int(update_wallet)}})
                    self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": wallet2 - int(update_wallet)}})
                    return await ctx.send(embed=embed)
            except KeyError:
                name = 'rob_activity'
                name2 = 'in_jail'
                value = 'true'
                value2 = 'no'
                self.db.mycol.update_one({"_id":user.id}, {'$set':{name: value}})
                self.db.mycol.update_one({"_id":user.id}, {'$set':{name2: value2}})
                return await ctx.send("Please run the command again.")
        except KeyError:
            name = 'rob_activity'
            name2 = 'in_jail'
            value = 'true'
            value2 = 'no'
            self.db.mycol.update_one({"_id":ctx.author.id}, {'$set':{name: value}})
            self.db.mycol.update_one({"_id":ctx.author.id}, {'$set':{name2: value2}})
            return await ctx.send("Please run the command again.")

    @commands.hybrid_command(aliases=['ac'])
    @commands.guild_only()
    @commands.is_owner()
    @commands.before_invoke(record_usage)
    async def addcoins(self, ctx, amount = None, user: discord.Member = None):
        "Add coins to users"
        transactions = f'{amount} coins has been added to wallet by {ctx.author.name}.'
        if user is None:
            user = ctx.author
        if amount is None:
            return await ctx.send("Please add the amount of coins you want to add.")
        
        amount = int(amount)

        find = self.db.mycol.find_one({"_id": user.id})
        if find is None:
            return await ctx.send("User don't have a account. Please use `^create` to create an account!")
        if amount < 0:
            return await ctx.send("Amount should not be less than 0.")
        
        wallet = find["wallet"]
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": wallet + amount}})
        self.db.mycol.update_one({"_id": user.id}, {"$push": {"description": transactions}})
        
        check = self.db.mycol.find_one({"_id": user.id})
        wallet1 = check["wallet"]
        bank1 = check["bank"]
        maxbank1 = check["maxbank"]

        em=discord.Embed(title='Your Balance',description='',color=discord.Color.random())
        em.add_field(name='Wallet', value=wallet1)
        em.add_field(name='Bank',value=f'{bank1}/{maxbank1}')
        # em.add_field(name='Transactions', value=description)
        em.set_thumbnail(url=user.display_avatar.url)

        await user.send(embed=em)
        await ctx.send(f"**{amount}** coins has been added to **{user}**")
    
    @commands.hybrid_command(aliases=['rc'])
    @commands.guild_only()
    @commands.is_owner()
    @commands.before_invoke(record_usage)
    async def removecoins(self, ctx, amount = None, user: discord.Member = None):
        "Remove Coins from Users."
        if user is None:
            user = ctx.author
        if amount is None:
            return await ctx.send("Please add the amount of coins you want to remove.")
        
        amount = int(amount)

        find = self.db.mycol.find_one({"_id": user.id})
        if find is None:
            return await ctx.send("User don't have a account. Please use `^create` to create an account!")
        if amount < 0:
            return await ctx.send("Amount should not be less than 0.")
        
        wallet = find["wallet"]
        self.db.mycol.update_one({"_id": user.id}, {"$set": {"wallet": wallet - amount}})
        
        check = self.db.mycol.find_one({"_id": user.id})
        wallet1 = check["wallet"]
        bank1 = check["bank"]
        maxbank1 = check["maxbank"]

        em=discord.Embed(title='Your Balance',description='',color=discord.Color.random())
        em.add_field(name='Wallet', value=wallet1)
        em.add_field(name='Bank',value=f'{bank1}/{maxbank1}')
        # em.add_field(name='Transactions', value=description)
        em.set_thumbnail(url=user.display_avatar.url)

        await user.send(embed=em)
        await ctx.send(f"**{amount}** coins has removed from **{user}**")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def daily(self, ctx):
        "Get your Daily Reward!"
        user = ctx.author
        find =  self.db.mycol.find_one(user.id)
        if find is not None:
            amount = 2000
            wallet = find["wallet"]
            start = find["daily_start"]
            if start == "yes":
                return await ctx.send("You're already claimed your Daily coins.")
            
            self.db.mycol.update_one({"_id":user.id}, {"$set": {"wallet": wallet + amount}})
            self.db.mycol.update_one({"_id":user.id}, {"$set":{"daily_start": "yes"}})
            await ctx.send(f'You have successfully claimed your Daily coins - **{amount}**.')

            while True:
                await asyncio.sleep(21600)
                user_find = self.db.mycol.find_one(user.id)
                daily = user_find["daily"]
                if daily == 0:
                    await user.send("You can collect your Daily coins now!")
                    self.db.mycol.update_one({"_id":user.id}, {"$set":{"daily": 86400}})
                    self.db.mycol.update_one({"_id":user.id}, {"$set":{"daily_start": "no"}})
                    break
                self.db.mycol.update_one({"_id":user.id}, {"$set":{"daily": daily - 21600}})
                continue
        else:
            return await ctx.send("You do not have an account. Use `^create` to create an account.")
    
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.before_invoke(record_usage)
    async def weekly(self, ctx):
        """Get Your Weekly Coins!"""
        check1 = topgg_votecheck(ctx.author)
        check2 = dbl_votecheck(ctx.author)
        print(check1, check2)

        if check1 is True and check2 is True:
            find =  self.db.mycol.find_one(ctx.author.id)
            if find is not None:
                amount = 6000
                wallet = find["wallet"]
                start = find["weekly_start"]
                if start == "yes":
                    return await ctx.send("You're already claimed your Weekly coins.")
                
                self.db.mycol.update_one({"_id":ctx.author.id}, {"$set": {"wallet": wallet + amount}})
                self.db.mycol.update_one({"_id":ctx.author.id}, {"$set":{"weekly_start": "yes"}})
                await ctx.send(f'You have successfully claimed your Weekly coins - **{amount}**.')

                while True:
                    await asyncio.sleep(21600)
                    user_find = self.db.mycol.find_one(ctx.author.id)
                    week = user_find["weekly"]
                    if week == 0:
                        self.db.mycol.update_one({"_id":ctx.author.id}, {"$set":{"weekly": 604800}})
                        self.db.mycol.update_one({"_id":ctx.author.id}, {"$set":{"weekly_start": "no"}})
                        break
                    self.db.mycol.update_one({"_id":ctx.author.id}, {"$set":{"weekly": week - 21600}})
                    continue
            else:
                return await ctx.send("You do not have an account. Use `^create` to create an account.")
        elif check1 == "error" or check2 == "error":
            return await ctx.send("Please wait an hour and try again.")
        else:
            av_button = discord.ui.Button(label='DiscordBotList', url = 'https://discordbotlist.com/bots/aromic/upvote')
            av_but = discord.ui.Button(label="Top.gg", url = "https://top.gg/bot/1055437102042599445/vote")
            view = discord.ui.View()
            view.add_item(av_button)
            view.add_item(av_but)
            embed = discord.Embed(title="",description="🛑 | Unfortunately this command is vote locked and you'll need to vote for Aromic!", color = discord.Color.random())
            return await ctx.send(embed=embed, view=view)

    # @commands.hybrid_command()
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def account(self, ctx):
    #     user = ctx.author
    #     guild = ctx.guild
    #     me = ctx.me
    #     overwrites = {
    #         guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
    #         user: discord.PermissionOverwrite(read_messages=True, send_messages= True),
    #         me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    #     }
    #     numbers=['1️⃣', '2️⃣','3️⃣', '❌']

    #     c = self.db.mycol.find_one({"_id":ctx.author.id})

    #     if c is not None:
    #         wallet = c['wallet']
    #         bank = c['bank']
    #         maxbank = c['maxbank']
    #         transactions = c['description']
    #         uniq = c['unique_id']
    #         pasw = c['password']

    #         p = "*" * len(pasw)
    #         uniq12 = "*" * len(str(uniq))

    #         if transactions == []:
    #             transactions = 'No transactions are done.'

    #         channel = await guild.create_text_channel(f'{user}', overwrites=overwrites)
    #         await ctx.send(f'To login into you account go to {channel}{channel.mention}.')
    #         await channel.send(f"{user.mention}")
    #         await asyncio.sleep(1)
    #         await channel.send("Enter Password: ")

    #         def check(m):
    #             return m.author == ctx.author and m.channel == channel

    #         try:
    #             while True:
    #                 message = await self.bot.wait_for('message', timeout=20.0, check = check)
    #                 if c['password'] == message.content:
    #                     await channel.send(f"Login Successful! You can return to {ctx.channel.mention}")
    #                     await asyncio.sleep(2)
    #                     await channel.delete()
    #                     break
    #                 else:
    #                     await channel.send("Incorrect Password.")
    #                     continue

                
    #             embed = discord.Embed(title = 'What do you want to check?', description = '1. Profile\n2. Balance\n3. Transactions', color = discord.Color.random())
    #             embed.set_footer(text = 'Just react to the number you want to check in the chat.')
    #             msg = await ctx.send(embed = embed)

    #             for number in numbers:
    #                 await msg.add_reaction(number)

    #             while True:
    #                 def react(reaction, user):
    #                     return user != self.bot.user and user == ctx.author and (str(reaction.emoji) in numbers)
                    
    #                 response,_ =await self.bot.wait_for("reaction_add",check=react,timeout=30)

    #                 if response.emoji == '1️⃣':
    #                     embed = discord.Embed(title=f"{ctx.author.name}'s Profile", color = discord.Color.random())
    #                     embed.add_field(name='Wallet', value=wallet)
    #                     embed.add_field(name='Bank',value=f'{bank}/{maxbank}')
    #                     embed.set_thumbnail(url=user.display_avatar.url)
    #                     embed.add_field(name='Transactions', value=f'{transactions}')
    #                     embed.add_field(name='Password', value=f'{p}')
    #                     embed.add_field(name='Unique ID', value=f'{uniq12}')
    #                     embed.set_footer(text = '* For security reasons, password and unique id was hidden.')
    #                     await ctx.send(embed= embed)
    #                     await asyncio.sleep(3)
    #                     one_msg = await ctx.send('Need to check anything else?')

    #                     for number in numbers:
    #                         await one_msg.add_reaction(number)
    #                     continue

    #                 elif response.emoji == '2️⃣':
    #                     em=discord.Embed(color=discord.Color.random())
    #                     em.add_field(name='Wallet', value=wallet)
    #                     em.add_field(name='Bank',value=f'{bank}/{maxbank}')
    #                     em.set_author(name='Your Balance')
    #                     em.set_thumbnail(url=user.display_avatar.url)
    #                     await ctx.send(embed=em)
    #                     await asyncio.sleep(4)
    #                     two_msg = await ctx.send('Need to check anything else?')

    #                     for number in numbers:
    #                         await two_msg.add_reaction(number)
    #                     continue

    #                 elif response.emoji == '3️⃣':
    #                     em=discord.Embed(description='**Transactions**',color=discord.Color.random())

    #                     for i, transa in enumerate(transactions[::-1][:10]):
    #                         em.add_field(name='', value=f"{i+1}. {transa}", inline=False)

    #                     em.set_thumbnail(url=user.display_avatar.url)
    #                     await ctx.send(embed=em)
    #                     await asyncio.sleep(4)
    #                     three_msg = await ctx.send('Need to check anything else?')

    #                     for number in numbers:
    #                         await three_msg.add_reaction(number)
    #                     continue
                    
    #                 elif response.emoji == '❌':
    #                     await ctx.send('Logging off...')
    #                     await asyncio.sleep(4)
    #                     await ctx.send('Account logged off.. Use the command again to check the account information.')
    #                     break

    #         except asyncio.TimeoutError:
    #             return await ctx.send('You took too long to respond.')

    #     else:
    #         await ctx.send(f'You dont have an account. Type `^create` to create an account.')

    # @commands.hybrid_command()
    # @commands.guild_only()
    # @commands.is_owner()
    # @commands.before_invoke(record_usage)
    # async def add_items(self, ctx, name:str, *, id:str, desc:str, cost:int, items):
    #     await self.create_shop(name, id, desc,  cost, items)
    #     await ctx.send(f'**{name}** added to the shop.')

    # # @commands.hybrid_command()
    # # @commands.guild_only()
    # # @commands.before_invoke(record_usage)
    # # async def shop(self, ctx):
    # #     """Shows all items available on Shop"""

    # #     find = self.db.shop.find({})
        
    # #     embed = discord.Embed(title='Shop', color=discord.Color.random())

    # #     for i in find:
            
    # #         if i["items"] == 'infinite':
    # #             embed.add_field(name=f"{i['name']} - ${i['cost']}", value=f'{i["desc"]}', inline = False)
    # #         else:
    # #             embed.add_field(name=f"{i['name']} - ${i['cost']} - `{i['items']}/{i['max_items']}`", value=f'{i["desc"]}', inline = False)
    # #     await ctx.send(embed=embed)
        
    # @commands.hybrid_command()
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def buy(self, ctx, item_name:str = None, amount:int = None):
    #     """Buy item from shop."""
    #     owner = 853506728519532544
    #     if item_name is None:
    #         return await ctx.send("Mention item name to buy.")
        
    #     if amount is None:
    #         amount = 1
       
    #     lower_item = item_name.lower()
    #     user = ctx.author
        
    #     find = self.db.mycol.find_one({"_id":user.id})
    #     find2 = self.db.shop.find_one({"_id":item_name})######
    #     find3 = self.db.inventory.find_one({"_id":user.id})
        
    #     if find is None:
    #         return await ctx.send("You do not have an account. Use `^create` to create one.")
    #     if find2 is None:
    #         return await ctx.send(f"No item named **{item_name}** was available in the shop.")
        
    #     wallet = find["wallet"]
    #     name = find2["name"]
    #     cost = find2["cost"]
    #     items = find2["items"]
    #     max_items = find2["max_items"]
        
    #     if wallet < cost:
    #         return await ctx.send(f"You do not have enough coins to buy the **{name}**")
        
    #     if find3 is None:
    #         return await ctx.send("You do not have an account. Use `^create` to create an account.")
        
    #     if type(items) == str and items == 'infinite':
    #         try:
    #             check = find3[name]
    #             new_data = f'{lower_item}'
    #             add = check + amount
    #             self.db.inventory.update_one({"_id":user.id}, {'$set':{f'{new_data}':int(f'{add}')}})
    #             self.db.mycol.update_one({"_id":user.id},{"wallet": wallet-cost})

    #         except KeyError:
    #             new_data = f'{lower_item}'
    #             new_amount = f'{amount}'
    #             self.db.inventory.update_one({"_id":user.id}, {'$set':{f'{new_data}':int(f'{new_amount}')}})
    #             self.db.mycol.update_one({"_id":user.id},{'$set':{"wallet": wallet-cost}})
        
    #     elif type(items)  == int:
    #         try:
    #             check = find3[name]
    #             new_data = f'{lower_item}'
    #             add = check + amount
    #             self.db.inventory.update_one({"_id":user.id}, {'$set':{f'{new_data}':int(f'{add}')}})
    #             self.db.shop.update_one({"_id":user.id}, {"$set":{"items": items-amount}})
    #             self.db.mycol.update_one({"_id":user.id},{"wallet": wallet-cost})

    #         except KeyError:
    #             new_data = f'{lower_item}'
    #             new_amount = f'{amount}'
    #             self.db.inventory.update_one({"_id":user.id}, {'$set':{f'{new_data}':int(f'{new_amount}')}})
    #             self.db.shop.update_one({"_id":user.id}, {"$set":{"items": items-amount}})
    #             self.db.mycol.update_one({"_id":user.id},{'$set':{"wallet": wallet-cost}})
                
    #     await ctx.send(f"You have successfully brought **{name}**")
        
        
    # @commands.hybrid_command()
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def use(self, ctx, item_name:str=None,amount:int=None):
    #     user = ctx.author
    #     if item_name is None:
    #         return await ctx.send("Please enter item name to use next time.")
    #     if amount is None:
    #         amount = 1
        
    #     find = self.db.mycol.find_one({"_id":user.id})
    #     find2 = self.db.shop.find_one({"_id":item_name})
    #     find3 = self.db.inventory.find_one({"_id":user.id})
        
    #     if find or find3 is None:
    #         return await ctx.send("You do not have an account. Use `^create` to create an account.")
        
    #     max_bank = find['maxbank']
    #     str_or_int = find2['items']
    #     item = find3[item_name]

    #     self.db.inventory.update_one({"_id":user.id}, {"$set":{}})


        # find_inv = self.db.my_colfind_one({"_id":user.id})
        # find_item_name = find_inv[item_name]
   

        # if find_inv is None:
        #     self.db.inventory.insert_one({"_id":user.id})
        # if find_item_name is None:
        #     return await ctx.send("The item you entered is invalid or not avalible in your inventory.")
        # if item_name == "banknote":
        #     user_data = self.db.inventory.find_one({"_id":user.id})
        #     bank_note = user_data["banknote"]
        #     if bank_note>amount:
        #         return await ctx.send(f"The given input is larger than the number of {item_name} avaliable in your inventory")
        #     else:
        #         self.db.inventory.update_one({"_id": user.id},{"set":{item_name:-amount}})
        #         self.db.mycol.update_one({"_id": user.id},{"set":{"maxbank":+1000}})
        #         return await ctx.send("Succesfully increased your max balan")

    # @commands.hybrid_command(aliases=["elb"])
    # @commands.guild_only()
    # @commands.before_invoke(record_usage)
    # async def leaderboard(self, ctx):
    #     wallet = self.db.mycol.find().sort("wallet", pymongo.DESCENDING)
    #     bank = self.db.mycol.find().sort("bank", pymongo.DESCENDING)
    #     select = Select(placeholder="Choose an option",
    #                     options=[
    #                         discord.SelectOption(label="Wallet", emoji="👛"),
    #                         discord.SelectOption(label="Bank", emoji="🏦")
    #                     ])
    #     view=View()
    #     view.add_item(select)
    #     embed=discord.Embed(title="Economy Leaderboard", description="To check the Economy Leaderboard please select an option below on the menu.",color=discord.Color.random())
    #     await ctx.send(embed=embed, view=view)
    #     for x in bank, wallet:

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))