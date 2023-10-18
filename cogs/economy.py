import discord, asyncio, random, string , requests, json
from discord.ext import commands
from discord import app_commands,Interaction
from mongo import db
from config import *

password = ''.join(random.choice(string.ascii_letters) for i in range(10))
default = password
uniq_pass = random.randint(100000, 999999)

async def record_usage(self, ctx):
    channel_id = "COMMAND_USAGE_CHANNEL_ID"
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
            "prefix": "DEFAULT_PREFIX"
            })
        return "DEFAULT_PREFIX"

def topgg_votecheck(user):
    url = f"https://top.gg/api/bots/BOT_ID/check?userId={user.id}"
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
    response = requests.get(f'https://discordbotlist.com/api/v1/bots/BOT_ID/upvotes', headers=headers)
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
        c =  self.db.mycol.find_one({"_id":interaction.user.id})
        
        if c is None:
            await self.create_account(interaction.user.id)
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

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
