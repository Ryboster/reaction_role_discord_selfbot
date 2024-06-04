# bot_events.py
import discord
import random # For dice rolls
import re # For fetching data from strings

from bot import ReactionRole, Victims
from discord.ext import commands
from insults import INSULTS

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.Cog.listener()
    async def on_ready(self):
        ''' Define behaviour on startup '''
        print('Bot is ready.')
        
    @commands.Cog.listener()
    async def on_message(self,message):
        ''' Simple chat commands '''
        await self.bot.process_commands(message)
        victims = Victims.retrieve_just_victims()

        if message.content.startswith('!!mpg'):
            distance = re.search(f'\d+', str(message.content))
            price = 1.4
            mpg = 36
            burnt_gallons = int(distance[0])/mpg
            burnt_litres = burnt_gallons*4.5

            await message.channel.send(f'''for a journey of {int(distance[0])} miles, with mpg of 36, you'll burn {round(burnt_gallons, 2)} gallons({burnt_litres}l), which will cost you {price*burnt_litres} pounds''')

        if message.author.id in victims:
            roll = random.randint(0, 100)
            abuse_type = Victims.get_abuse_type_for_victim(message.author.id)
            chance = Victims.get_chance_for_victim(message.author.id)

            if abuse_type == 1 and chance >= roll:
                insult = INSULTS[random.randint(0, (len(INSULTS) -1))]
                await message.reply(insult)

            elif abuse_type == 2 and chance >= roll:
                await message.delete()
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        ''' On added reaction, add corresponding role '''

        reaction_roles = ReactionRole.retrieve_reaction_roles()
        for tup in reaction_roles:
            if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
                try:
                    guild = self.bot.get_guild(payload.guild_id)
                    channel = self.bot.get_channel(payload.channel_id)
                    user = guild.get_member(payload.user_id)
                    role = discord.utils.get(guild.roles, id=int(tup[2]))
                    await user.add_roles(role)
                except Exception as e:
                    await self.bot.get_channel(payload.channel_id).send(e)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        ''' On removed reaction, remove corresponding role '''

        reaction_roles = ReactionRole.retrieve_reaction_roles()
        for tup in reaction_roles:
             if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
                try:
                    guild = self.bot.get_guild(payload.guild_id)
                    channel = self.bot.get_channel(payload.channel_id)
                    user = guild.get_member(payload.user_id)
                    role = discord.utils.get(guild.roles, id=int(tup[2]))
                    await user.remove_roles(role)
                except Exception as e:
                    await self.bot.get_channel(payload.channel_id).send(e)
