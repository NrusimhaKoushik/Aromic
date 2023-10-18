import discord, random, string, math
import typing
import wavelink
from config import *
from discord.ui import button, Button, View
from discord.ext import commands
from wavelink.ext import spotify
from mongo import db

class MyView(View):
    def __init__(self):
        super().__init__(timeout = None)
        self.db = db

    @button(label='Volume Down', style=discord.ButtonStyle.grey, emoji = "🔉")
    async def volume_down_button_callback(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)
        vc: wavelink.Player = interaction.guild.voice_client

        to = vc.volume - 10
        if to < 10:
            return await interaction.response.send_message("Volume cannot be changed below `10`.", ephemeral=True)
        else:
            pass

        if player is not None:
            try:
                if not interaction.user.voice.channel:
                    return await interaction.response.send_message("You need to join the voice channel to change the music volume.",ephemeral=True)
            except AttributeError:
                return await interaction.response.send_message("You need to join the voice channel to change the music volume.",ephemeral=True)
            if player.is_playing():
                await player.set_volume(to)
                mbed = discord.Embed(title="", description=f"Changed Volume to **{to}**", color=discord.Color.from_rgb(255, 255, 255))
                await interaction.response.send_message(embed=mbed, ephemeral=True)
            else:
                return await interaction.response.send_message("No songs are playing right now!",ephemeral=True)
        else:
            return await interaction.response.send_message("Bot is not connected to any voice channel.", ephemeral=True)

    @button(label='Pause', style=discord.ButtonStyle.grey, emoji = "⏸️")
    async def pause_resume_button_callback(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)

        if player is not None:
            try:
                if not interaction.user.voice.channel:
                    return await interaction.response.send_message("You need to join the voice channel to pause the music.",ephemeral=True)
            except AttributeError:
                return await interaction.response.send_message("You need to join the voice channel to pause the music.",ephemeral=True)
            if not player.is_paused():
                if player.is_playing():
                    await player.pause()
                    button.emoji = '▶️'
                    button.label = 'Resume'
                    return await interaction.response.edit_message(view=self)
                else:
                    return await interaction.response.send_message("No songs are playing right now!",ephemeral=True)
            else:
                await player.resume()
                button.emoji = '⏸️'
                button.label = 'Pause'
                return await interaction.response.edit_message(view=self)
        else:
            return await interaction.response.send_message("Bot is not connected to any voice channel.", ephemeral=True)
    
    @button(label='Stop', style=discord.ButtonStyle.grey, emoji = "⏹️")
    async def stop_button_callback(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)
        vc: wavelink.Player = interaction.guild.voice_client

        if player is not None:
            try:
                if not interaction.user.voice.channel:
                    return await interaction.response.send_message("You need to join the voice channel to stop the music.",ephemeral=True)
            except AttributeError:
                return await interaction.response.send_message("You need to join the voice channel to stop the music.",ephemeral=True)
            if player.is_playing():
                await player.stop()
                vc.queue.clear()
                self.db.play_channel.delete_many({"guild":interaction.guild.id})
                for item in self.children:
                    item.disabled = True
                return await interaction.response.edit_message(view=self)
            else:
                return await interaction.response.send_message("No songs are playing right now!",ephemeral=True)
        else:
            return await interaction.response.send_message("Bot is not connected to any voice channel.", ephemeral=True)
    
    @button(label='Queue', style=discord.ButtonStyle.grey, emoji='📃')
    async def queue_button_callback(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)

        if player is not None:
            vc: wavelink.Player = interaction.guild.voice_client
            if not vc.queue.is_empty:
                song_counter = 0
                songs = []
                queue = vc.queue.copy()

                embed = discord.Embed(title = "Queue List")

                for song in queue:
                    song_counter += 1
                    songs.append(song)

                    days = int(math.floor(song.duration/(1000*60*60*24)%24))
                    hours = int(math.floor(song.duration/(1000*60*60)%24))
                    minutes = int(math.floor(song.duration/(1000*60)%60))
                    seconds = int(math.floor(song.duration/1000%60))

                    if days == 0:
                        duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                    elif hours == 0:
                        duration = f'{minutes:02d}:{seconds:02d}'
                    elif minutes == 0:
                        duration = f'{seconds:02d}'
                    else:
                        duration = f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'

                    embed.add_field(name=f'{song_counter}. {song.title}', value = f'Duration: `{duration}`', inline=False)

                await interaction.response.send_message(embed=embed)
            else:
                self.db.play_channel.delete_many({"guild":interaction.guild.id})
                await interaction.response.send_message("Queue is empty.", ephemeral=True)
        else:
            return await interaction.response.send_message("Bot is not connnected to any voice channel.", ephemeral=True)

    @button(label='Volume Up', style=discord.ButtonStyle.grey, emoji = "🔊", row=2)
    async def volume_up_button_callback(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)
        vc: wavelink.Player = interaction.guild.voice_client

        to = vc.volume + 10
        if to > 100:
            return await interaction.response.send_message("Volume should not be more than `100`.", ephemeral=True)
        else:
            pass

        if player is not None:
            try:
                if not interaction.user.voice.channel:
                    return await interaction.response.send_message("You need to join the voice channel to change the music volume.",ephemeral=True)
            except AttributeError:
                return await interaction.response.send_message("You need to join the voice channel to change the music volume.",ephemeral=True)
            if player.is_playing():
                await player.set_volume(to)
                mbed = discord.Embed(title="", description=f"Changed Volume to **{to}**", color=discord.Color.from_rgb(255, 255, 255))
                await interaction.response.send_message(embed=mbed, ephemeral=True)
            else:
                return await interaction.response.send_message("No songs are playing right now!",ephemeral=True)
        else:
            return await interaction.response.send_message("Bot is not connected to any voice channel.", ephemeral=True)
    
    @button(label='Skip', style=discord.ButtonStyle.grey, emoji='⏭️', row=2)
    async def skip_button_callback(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)

        if player is not None:
            if player.is_playing():
                try:
                    if not interaction.user.voice.channel:
                        return await interaction.response.send_message("You need to join the voice channel to skip the music.",ephemeral=True)
                except AttributeError:
                    return await interaction.response.send_message("You need to join the voice channel to skip the music.",ephemeral=True)
                vc: wavelink.Player = interaction.guild.voice_client
                if not vc.queue.is_empty:
                    await vc.stop()
                    await interaction.response.send_message("Song skipped.")
                else:
                    await vc.stop()
                    self.db.play_channel.delete_many({"guild":interaction.guild.id})
                    await interaction.response.send_message("Nothing in the queue to play. Add some songs", ephemeral=True)
            else:
                return await interaction.response.send_message("Nothing playing right now.", ephemeral=True)
        else:
            return await interaction.response.send_message("Bot is not connnected to any voice channel.", ephemeral=True)
    
    @button(label='Now Playing', style=discord.ButtonStyle.grey, emoji='🎵', row=2)
    async def now_playing_button_callbabck(self, interaction:discord.Interaction, button:Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild.id)
        vc: wavelink.Player = interaction.guild.voice_client
        if player is not None:
            if player.is_playing():
                try:
                    if not interaction.user.voice.channel:
                        return await interaction.response.send_message("You need to join the voice channel to get datails of the current music.",ephemeral=True)
                except AttributeError:
                    return await interaction.response.send_message("You need to join the voice channel to get datails of the current music.",ephemeral=True)
                days = int(math.floor(player.current.duration/(1000*60*60*24)%24))
                hours = int(math.floor(player.current.duration/(1000*60*60)%24))
                minutes = int(math.floor(player.current.duration/(1000*60)%60))
                seconds = int(math.floor(player.current.duration/1000%60))

                if days == 0:
                    duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                elif hours == 0:
                    duration = f'{minutes:02d}:{seconds:02d}'
                elif minutes == 0:
                    duration = f'{seconds:02d}'
                else:
                    duration = f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'

                embed = discord.Embed(title = "PLAYER 🎶",description = f"Now playing: **[{player.current.title}]({player.current.uri})**",color = discord.Color.from_rgb(255, 255, 255))
                embed.add_field(name = '🙋 Requested by', value = f'{interaction.user.mention}')
                embed.add_field(name = '🎹 Music author', value = f"`{player.current.author}`")
                embed.add_field(name = '⏰ Music duration', value = f'`{duration}`')

                await interaction.response.send_message(embed=embed)
            else:
                return await interaction.response.send_message("Nothing playing right now.", ephemeral=True)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db
        bot.loop.create_task(self.create_nodes())
    
    async def create_nodes(self):
        await self.bot.wait_until_ready()

        sc = spotify.SpotifyClient(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
        
        node: wavelink.Node = wavelink.Node(uri=LAVALINK_HOST, password=LAVALINK_PASSWORD, secure=False)
        await wavelink.NodePool.connect(client=self.bot, nodes=[node], spotify=sc)
        wavelink.Player.autoplay = False

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        vc: wavelink.Player = payload.player

        try:
            next_song = vc.queue.get()

            find = self.db.play_channel.find_one({"guild":vc.guild.id})
            channel = find["channel"]
            user = find['user']
            ctx = vc.guild.get_channel(int(channel))
            author = vc.guild.get_member(int(user))

            days = int(math.floor(next_song.duration/(1000*60*60*24)%24))
            hours = int(math.floor(next_song.duration/(1000*60*60)%24))
            minutes = int(math.floor(next_song.duration/(1000*60)%60))
            seconds = int(math.floor(next_song.duration/1000%60))

            if days == 0:
                duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif hours == 0:
                duration = f'{minutes:02d}:{seconds:02d}'
            elif minutes == 0:
                duration = f'{seconds:02d}'
            else:
                duration = f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'

            embed = discord.Embed(title = "PLAYER 🎶",description = f"Now playing: **{next_song.title}**",color = discord.Color.from_rgb(255, 255, 255))
            embed.add_field(name = '🙋 Requested by', value = f'{author.mention}')
            
            try:
                embed.add_field(name = '🎹 Music author', value = f"`{next_song.author}`")
            except AttributeError:
                embed.add_field(name = '🎹 Artist', value = f"`{next_song.artists}`")

            embed.add_field(name = '⏰ Music duration', value = f'`{duration}`')

            try:
                embed.set_thumbnail(url = next_song.thumbnail)
            except AttributeError:
                embed.set_thumbnail(url = next_song.images[0])
            
            await vc.play(next_song)
            await ctx.send(embed=embed)

            self.db.play_channel.delete_one({"song":next_song.title})
        except wavelink.exceptions.QueueEmpty:
            self.db.play_channel.delete_many({"guild":vc.guild.id})

    @commands.hybrid_command(name="join", aliases=["connect", "summon"])
    async def join_command(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]=None):
        """Invite me to play some Music."""
        try:
            if channel is None:
                channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send('Join a voice channel and try again.')
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            if player.is_connected():
                return await ctx.send("Bot is already connected to a voice channel")
            
        await channel.connect(cls=wavelink.Player)
        mbed=discord.Embed(title=f"Connected to {channel.mention}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)

    @commands.hybrid_command(name="leave", alises=["disconnect"])
    async def leave_command(self, ctx: commands.Context):
        """Disconnect me from a voice channel."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            if not ctx.author.voice.channel:
                return await ctx.send("You need to join the voice channel to disconnect me.")
            if player.is_connected():
                await player.disconnect()
                self.db.play_channel.delete_many({"guild": ctx.guild.id})
                mbed = discord.Embed(title="Disconnected", color=discord.Color.from_rgb(255, 255, 255))
                await ctx.send(embed=mbed)
        else:
            return await ctx.send("Bot is not connected to any voice channel")
    
    @commands.hybrid_command(name="play")
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def play_command(self, ctx: commands.Context, *, search:str):
        """Play your favourite Music."""
        query = await wavelink.YouTubeTrack.search(search)

        id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        default = id

        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send('Please join a voice channel and try again.')
        
        try:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player, self_deaf=True)
        except discord.ClientException:
            vc: wavelink.Player = ctx.voice_client

        self.db.play_channel.insert_one({"_id":default, "song":query[0].title, "guild":ctx.guild.id, "channel": ctx.channel.id, "user":ctx.author.id})

        if vc.queue.is_empty and not vc.is_playing():
            find = self.db.play_channel.find_one({"guild":vc.guild.id})
            user = find['user']
            author = vc.guild.get_member(int(user))

            days = int(math.floor(query[0].duration/(1000*60*60*24)%24))
            hours = int(math.floor(query[0].duration/(1000*60*60)%24))
            minutes = int(math.floor(query[0].duration/(1000*60)%60))
            seconds = int(math.floor(query[0].duration/1000%60))

            if days == 0:
                duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif hours == 0:
                duration = f'{minutes:02d}:{seconds:02d}'
            elif minutes == 0:
                duration = f'{seconds:02d}'
            else:
                duration = f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'

            embed = discord.Embed(title = "PLAYER 🎶",description = f"Now playing: **[{query[0].title}]({query[0].uri})**",color = discord.Color.from_rgb(255, 255, 255))
            embed.add_field(name = '🙋 Requested by', value = f'{author.mention}')
            embed.add_field(name = '🎹 Music author', value = f"`{query[0].author}`")
            embed.add_field(name = '⏰ Music duration', value = f'`{duration}`')
            embed.set_thumbnail(url = query[0].thumbnail)

            await vc.play(query[0])
            await vc.set_volume(100)
            view = MyView()
            await ctx.send(embed=embed, view = view)
            self.db.play_channel.delete_one({"song":query[0].title})
        else:
            await vc.queue.put_wait(query[0])
            await ctx.send(f"**{query[0]}** added to the Queue.")
    
    @commands.hybrid_command(name="stop")
    async def stop_command(self, ctx: commands.Context):
        """Stop the Music Player."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        vc: wavelink.Player = ctx.guild.voice_client

        if player is not None:
            if not ctx.author.voice.channel:
                return await ctx.send("You need to join the voice channel to stop the music.")
            if player.is_playing():
                await player.stop()
                vc.queue.clear()
                self.db.play_channel.delete_many({"guild":ctx.guild.id})
                mbed = discord.Embed(title="Playback Stopped", color=discord.Color.from_rgb(255, 255, 255))
                return await ctx.send(embed=mbed)
            else:
                return await ctx.send("Nothing playing right now!")
        else:
            return await ctx.send("Bot is not connected to any voice channel.")
    
    @commands.hybrid_command(name="pause")
    async def pause_command(self, ctx: commands.Context):
        """Pause the Music Player."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            if not ctx.author.voice.channel:
                return await ctx.send("You need to join the voice channel to pause the music.")
            if player.is_playing():
                if not player.is_paused():
                    await player.pause()
                    mbed = discord.Embed(title="Playback Paused", color=discord.Color.from_rgb(255, 255, 255))
                    return await ctx.send(embed=mbed)
            else:
                return await ctx.send("Playback is already paused!")
        else:
            return await ctx.send("Bot is not connected to any voice channel.")
    
    @commands.hybrid_command(name="resume")
    async def resume_command(self, ctx: commands.Context):
        """Resume the Music Player."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            if not ctx.author.voice.channel:
                return await ctx.send("You need to join the voice channel to resume the music.")
            
            if player.is_paused():
                await player.resume()
                mbed = discord.Embed(title="Playback resumed", color=discord.Color.from_rgb(255, 255, 255))
                return await ctx.send(embed=mbed)
            else:
                return await ctx.send("No song was playing to resume.")
        else:
            return await ctx.send("Bot is not connnected to any voice channel.")

    @commands.hybrid_command(name="volume")
    async def volume_command(self, ctx: commands.Context, to: int):
        """Change the Volume of your interest."""
        if to > 100:
            return await ctx.send("Volume should be between 0 and 100.")
        if to < 1:
            return await ctx.send("Volume should be between 0 and 100.")
        if not ctx.author.voice:
            return await ctx.send(f"Join the channel to control volume of the player.")
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            
            if player.is_playing():
                await player.set_volume(to)
                mbed = discord.Embed(title="", description=f"Changed Volume to **{to}**", color=discord.Color.from_rgb(255, 255, 255))
                await ctx.send(embed=mbed)
            else:
                await ctx.send("Nothing playing right now.")
        else:
            return await ctx.send("Bot is not connnected to any voice channel.")
    
    @commands.hybrid_command(name="skip")
    async def skip_command(self, ctx):
        """Skip the current song."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            if player.is_playing():
                vc: wavelink.Player = ctx.guild.voice_client
                if not vc.queue.is_empty:
                    await vc.stop()
                    await ctx.send("Song skipped.")
                else:
                    await vc.stop()
                    self.db.play_channel.delete_many({"guild":ctx.guild.id})
                    await ctx.send("Nothing in the queue to play. Add some songs")
            else:
                await ctx.send("Nothing playing right now.")
        else:
            return await ctx.send("Bot is not connnected to any voice channel.")
        
    @commands.hybrid_command(name='queue')
    async def queue_command(self, ctx):
        """Get the songs queue list."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            vc: wavelink.Player = ctx.guild.voice_client
            if not vc.queue.is_empty:
                song_counter = 0
                songs = []
                queue = vc.queue.copy()

                embed = discord.Embed(title = "Queue List")

                for song in queue:
                    song_counter += 1
                    songs.append(song)

                    days = int(math.floor(song.duration/(1000*60*60*24)%24))
                    hours = int(math.floor(song.duration/(1000*60*60)%24))
                    minutes = int(math.floor(song.duration/(1000*60)%60))
                    seconds = int(math.floor(song.duration/1000%60))

                    if days == 0:
                        duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                    elif hours == 0:
                        duration = f'{minutes:02d}:{seconds:02d}'
                    elif minutes == 0:
                        duration = f'{seconds:02d}'
                    else:
                        duration = f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'

                    embed.add_field(name=f'{song_counter}. {song.title}', value = f'Duration: `{duration}`', inline=False)

                await ctx.send(embed=embed)
            else:
                self.db.play_channel.delete_many({"guild":ctx.guild.id})
                await ctx.send("Queue is empty.")
        else:
            return await ctx.send("Bot is not connnected to any voice channel.")
        
    @commands.hybrid_command(name='removesong')
    async def remove_command(self, ctx, *, index: int):
        """Remove the song from the Queue."""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if index <= 0:
            return await ctx.send("Number should not be less than or equal to 0.")

        if player is not None:
            vc: wavelink.Player = ctx.guild.voice_client
            if not vc.queue.is_empty:
                title = vc.queue[index - 1].title
                vc.queue.__delitem__(index - 1)
                await ctx.send(f"Removed **{title}** from the Query.")
                self.db.play_channel.delete_one({"song":title})
            else:
                await ctx.send("Queue is empty.")
        else:
            return await ctx.send("Bot is not connnected to any voice channel.")

    @commands.hybrid_command(name='playspotify', aliases=['spotify'])
    async def play_spotify(self, ctx, *, url:str = None):
        """Play spotify songs."""
        try:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                return await ctx.send('Join a voice channel and try again.')

            if url is None:
                return await ctx.send('Mention song url to play some music.')
            
            try:
                vc: wavelink.Player = await channel.connect(cls=wavelink.Player, self_deaf=True)
            except discord.ClientException:
                vc: wavelink.Player = ctx.voice_client
            
            tracks: list[spotify.SpotifyTrack] = await spotify.SpotifyTrack.search(query=url)
            if len(tracks) > 1:
                msg = await ctx.send("Decoding Playlist...")
            else:
                msg = await ctx.send("Searching spotify...")

            for i in tracks:
                if i == tracks[0]:
                    if not vc.is_playing():
                        continue
                    else:
                        await vc.put_wait(tracks[0])
                        self.db.play_channel.insert_one({"_id":''.join(random.choice(string.ascii_letters) for i in range(10)), "song":tracks[0].title, "guild":ctx.guild.id, "channel": ctx.channel.id, "user":ctx.author.id})
                await vc.queue.put_wait(i)
                self.db.play_channel.insert_one({"_id":''.join(random.choice(string.ascii_letters) for i in range(10)), "song":i.title, "guild":ctx.guild.id, "channel": ctx.channel.id, "user":ctx.author.id})

            days = int(math.floor(tracks[0].duration/(1000*60*60*24)%24))
            hours = int(math.floor(tracks[0].duration/(1000*60*60)%24))
            minutes = int(math.floor(tracks[0].duration/(1000*60)%60))
            seconds = int(math.floor(tracks[0].duration/1000%60))

            if days == 0:
                duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif hours == 0:
                duration = f'{minutes:02d}:{seconds:02d}'
            elif minutes == 0:
                duration = f'{seconds:02d}'
            else:
                duration = f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}'

            if not vc.is_playing():
                embed = discord.Embed(title = "PLAYER 🎶",description = f"Now playing: **[{tracks[0].title}]({url})**",color = discord.Color.from_rgb(255, 255, 255))
                embed.add_field(name = '🙋 Requested by', value = f'{ctx.author.mention}')
                embed.add_field(name = '🎹 Artist', value = f"`{tracks[0].artists[0]}`")
                embed.add_field(name = '⏰ Music duration', value = f'`{duration}`')
                embed.set_thumbnail(url = tracks[0].images[0])

                await vc.play(tracks[0])
                await msg.delete()
                await ctx.send(embed = embed)
            else:
                await vc.queue.put_wait(tracks[0])
        except Exception:
            return await ctx.send("No songs/playlists found. Try using `https://open.spotify.com/track(or)playlist` type links.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
