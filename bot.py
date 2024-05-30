import sys # For interacting with the operating system
sys.path.insert(0, 'discord.py-self')
import discord
from discord.ext import commands
from discord.errors import HTTPException

import asyncio
import json # for parsing config.json
import re # Regex for searching patterns
#import tracemalloc
#tracemalloc.start()

from db_manager import * # Database functions - Own module

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

    if message.content.startswith('!!mpg'):
        distance = re.search(f'\d+', str(message.content))
        price = 1.4
        mpg = 36
        gallon = 4.5
        litre = 1
        burnt_gallons = int(distance[0])/mpg
        burnt_litres = burnt_gallons*4.5

        await message.channel.send(f'''for a journey of {int(distance[0])} miles, with mpg of 36, you'll burn {round(burnt_gallons, 2)} gallons({burnt_litres}l), which will cost you {price*burnt_litres} pounds''')
        
@bot.event
async def on_raw_reaction_add(payload):
    '''On reaction, add role'''
    reaction_roles = retrieve_reactionroles_db(get_db_connection())
    for tup in reaction_roles:
        if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
            guild = bot.get_guild(payload.guild_id)
            channel = bot.get_channel(payload.channel_id)
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(tup[2]))
            await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    reaction_roles = retrieve_reactionroles_db(get_db_connection())
    for tup in reaction_roles:
         if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
            guild = bot.get_guild(payload.guild_id)
            channel = bot.get_channel(payload.channel_id)
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(tup[2]))
            await user.remove_roles(role)


@bot.command()
async def add_reaction_role(ctx, msg_id, reaction, role):
    ''' Register new watched message and assign reaction roles to it '''
    target_message = await ctx.fetch_message(int(msg_id))    
    register_new_watched_message(msg_id, ctx.channel.id, get_db_connection())
    role = int(str(role).replace('<', '').replace('>', '').replace('@', '').replace('&', ''))
    add_new_reaction_role(reaction, role, msg_id, get_db_connection())
    await target_message.add_reaction(reaction)
    await ctx.send(f'added reaction {reaction} to message {msg_id} ({target_message.content})')
    
@bot.command()
async def drop_db(ctx):
    ''' Hard reset database '''
    if ctx.author.id == ADMIN_ID:
        try:
            truncate_db(get_db_connection())
            await ctx.send("truncated database")
            initialize_db(get_db_connection())
            await ctx.send("database reset")
        except Exception as e:
            error_message = f"Error occurred while resetting database: {e}"
            await ctx.send(error_message)
    else:
        await ctx.send('nice try pleb')

@bot.command()
async def read_from_db(ctx):
    ''' Print out all values from database '''
    if ctx.author.id == ADMIN_ID:
        watched_messages = retrieve_messages_db(get_db_connection())
        await ctx.send(watched_messages)
        reaction_roles = retrieve_reactionroles_db(get_db_connection())
        await ctx.send(reaction_roles)
    else:
        await ctx.send('nice try pleb')


async def main():
    await bot.start(token)

try:
    initialize_db(get_db_connection())
    asyncio.run(main())
except KeyboardInterrupt:
    asyncio.run(bot.close())