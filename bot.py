### External Modules
import sys # For interacting with the operating system
import random # For dice rolls
import asyncio # For asynchronous operations
import json # For reading config file
import re # For fetching data from strings

### Discord Modules
sys.path.insert(0, 'discord.py-self')
import discord
from discord.ext import commands
from discord.errors import HTTPException


### Own modules
from reactionrole_db_manager import ReactionRoleManager # - Set of functions for ReactionRoles database interaction
from victims_db_manager import VictimManager # - Set of functions for Victims database interaction
from insults import INSULTS # - List of mild insults


ReactionRole = ReactionRoleManager()
Victims = VictimManager()

with open('config/config.json') as f:
    config = json.load(f)
    token = config['token']
    prefix = config['prefix']
    ADMIN_ID = int(config['ADMIN_ID'])
    bot = commands.Bot(command_prefix=prefix, self_bot=True)

@bot.event
async def on_ready():
    ''' Define behaviour on startup '''
    print('Bot is ready.')


@bot.event
async def on_message(message):
    ''' Simple chat commands '''
    await bot.process_commands(message)
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
            
        
@bot.event
async def on_raw_reaction_add(payload):
    ''' On added reaction, add role '''
    reaction_roles = ReactionRole.retrieve_reaction_roles()
    
    for tup in reaction_roles:
        if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
            guild = bot.get_guild(payload.guild_id)
            channel = bot.get_channel(payload.channel_id)
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(tup[2]))
            await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    ''' On removed reaction, remove role '''
    reaction_roles = ReactionRole.retrieve_reaction_roles()
    
    for tup in reaction_roles:
         if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
            guild = bot.get_guild(payload.guild_id)
            channel = bot.get_channel(payload.channel_id)
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(tup[2]))
            await user.remove_roles(role)


@bot.command()
async def bully(ctx, user: int, abuse_type: int, chance: int):
    ''' Register new member as victim '''
    guild = ctx.guild
    members = guild.members
    member_ids = [member.id for member in members]
    if user in member_ids:
        if abuse_type == 1 or abuse_type == 2:
            if chance > 0 and chance <= 100:
                response = Victims.add_new_victim(user, abuse_type, chance)
                await ctx.send(response)
            else:
                await ctx.send('ERROR: chance must be between 1 and 100')
        else:
            await ctx.send('ERROR: abuse type must be either 1 or 2')
    else:
        await ctx.send('ERROR: member not in server')

@bot.command()
async def liberate_victim(ctx, user: int):
    guild = ctx.guild
    members = [member.id for member in guild.members]
    if user in members:
        response = Victims.liberate_victim(user)
        await ctx.send(response)
    else:
        await ctx.send("ERROR: User not in server")


@bot.command()
async def add_reaction_role(ctx, msg_id, reaction, role):
    ''' Register new watched message and assign reaction roles to it '''
    target_message = await ctx.fetch_message(int(msg_id))    
    ReactionRole.register_new_watched_message(msg_id,ctx.channel.id)
    role = int(str(role).replace('<', '').replace('>', '').replace('@', '').replace('&', ''))
    ReactionRole.add_new_reaction_role(reaction, role, msg_id)
    await target_message.add_reaction(reaction)
    await ctx.send(f'added reaction {reaction} to message {msg_id} ({target_message.content})')
    
@bot.command()
async def drop_reactionroles(ctx):
    ''' Reset ReactionRoles db '''
    if ctx.author.id == ADMIN_ID:
        try:
            ReactionRole.drop_db()
            await ctx.send("truncated database")
            ReactionRole.__init__()
            await ctx.send("database back up")
        except Exception as e:
            error_message = f"Error occurred while resetting database: {e}"
            await ctx.send(error_message)
    else:
        await ctx.send('nice try pleb')

@bot.command()
async def drop_victims(ctx):
    ''' Reset victims db '''
    if ctx.author.id == ADMIN_ID:
        Victims.drop_db()
        await ctx.send('truncated database')
        Victims.__init__()
        await ctx.send('database back up')
    else:
        await ctx.send('nice try pleb')
        
@bot.command()
async def read_reactionroles(ctx):
    ''' Print out all values from database '''
    if ctx.author.id == ADMIN_ID:
        watched_messages = ReactionRole.retrieve_messages()
        await ctx.send(watched_messages)
        reaction_roles = ReactionRole.retrieve_reaction_roles()
        await ctx.send(reaction_roles)
    else:
        await ctx.send('nice try pleb')

@bot.command()
async def read_victims(ctx):
    if ctx.author.id == ADMIN_ID:
        victims = Victims.retrieve_table()
        await ctx.send(victims)
    else:
        await ctx.send('nice try pleb')


@bot.command()
async def get_just_victims(ctx):
    if ctx.author.id == ADMIN_ID:
        victims = Victims.retrieve_just_victims()
        await ctx.send(victims)
    else:
        await ctx.send('nice try pleb')


async def main():
    await bot.start(token)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    asyncio.run(bot.close())