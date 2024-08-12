### Discord selfbot
## Blazejowski, G. 2023


# Before starting, fill in the missing information in ./config/config.json

import sys # For interacting with the operating system
sys.path.insert(0, 'discord.py-self')

import discord
from discord.ext import commands
from discord.errors import HTTPException

import asyncio # For asynchronous operations
import json # for parsing config.json
import re # for finding set patterns


from db_manager import * # Database interface


### Define the bot object with information from config
with open('config/config.json') as f:
    config = json.load(f)
    token = config['token']
    PREFIX = config['prefix']
    ADMIN_ID = int(config['ADMIN_ID'])
    bot = commands.Bot(command_prefix=PREFIX, self_bot=True)


@bot.event
async def on_ready():
    ''' Behaviour on startup '''
    print('Bot is ready.')


@bot.event
async def on_message(message):
    ''' Callback function for when
        a message is sent '''
    
    await bot.process_commands(message)

    
@bot.event
async def on_raw_reaction_add(payload):
    ''' Callback function for when a
        reaction is added to a message '''
    
    reaction_roles = retrieve_reactionroles_db(get_db_connection())
    for tup in reaction_roles:
        if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
            guild = bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(tup[2]))
            await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    ''' Callback function for when a 
        reaction is removed from a message '''
        
    reaction_roles = retrieve_reactionroles_db(get_db_connection())
    for tup in reaction_roles:
         if int(payload.message_id) == int(tup[0]) and str(payload.emoji) == str(tup[1]):
            guild = bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(tup[2]))
            await user.remove_roles(role)



# Decorator for defining custom commands
# Commands take on the function names
@bot.command()
async def add_reaction_role(ctx, msg_id, reaction, role):
    ''' Register new watched message and
        assign reaction roles to it '''
    
    target_message = await ctx.fetch_message(int(msg_id))    
    register_new_watched_message(msg_id, ctx.channel.id, get_db_connection())
    role = int(str(role).replace('<', '').replace('>', '').replace('@', '').replace('&', ''))
    add_new_reaction_role(reaction, role, msg_id, get_db_connection())
    await target_message.add_reaction(reaction)
    await ctx.send(f'added reaction {reaction} to message {msg_id} ({target_message.content})')
    

@bot.command()
async def drop_db(ctx):
    ''' Wipe the database '''
    
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
    ''' Return all values from the database.
    
        NOTE: This will be sent as a message in
        the chat the command has been sent in.'''
    
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