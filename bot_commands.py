# bot_commands.py
from bot import ADMIN_ID, ReactionRole, Victims
from discord.ext import commands

@commands.command()
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
        
@commands.command()
async def liberate_victim(ctx, user: int):
    guild = ctx.guild
    members = [member.id for member in guild.members]
    if user in members:
        response = Victims.liberate_victim(user)
        await ctx.send(response)
    else:
        await ctx.send("ERROR: User not in server")
        
        
@commands.command()
async def add_reaction_role(ctx, msg_id, reaction, role):
    ''' Register new watched message and assign reaction roles to it  '''
    target_message = await ctx.fetch_message(int(msg_id))    
    ReactionRole.register_new_watched_message(msg_id,ctx.channel.id)
    role = int(str(role).replace('<', '').replace('>', '').replace('@', '').replace('&', ''))
    ReactionRole.add_new_reaction_role(reaction, role, msg_id)
    await target_message.add_reaction(reaction)
    await ctx.send(f'added reaction {reaction} to message {msg_id} ({target_message.content})')
    
    
@commands.command()
async def drop_reactionroles(ctx):
    ''' Reset ReactionRoles database '''
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
        
        
@commands.command()
async def drop_victims(ctx):
    ''' Reset victims db '''
    if ctx.author.id == ADMIN_ID:
        Victims.drop_db()
        await ctx.send('truncated database')
        Victims.__init__()
        await ctx.send('database back up')
    else:
        await ctx.send('nice try pleb')
        
        
@commands.command()
async def read_reactionroles(ctx):
    ''' Print out all values from database '''
    if ctx.author.id == ADMIN_ID:
        watched_messages = ReactionRole.retrieve_messages()
        await ctx.send(watched_messages)
        reaction_roles = ReactionRole.retrieve_reaction_roles()
        await ctx.send(reaction_roles)
    else:
        await ctx.send('nice try pleb')
        
        
@commands.command()
async def read_victims(ctx):
    if ctx.author.id == ADMIN_ID:
        victims = Victims.retrieve_table()
        await ctx.send(victims)
    else:
        await ctx.send('nice try pleb')
        
        
@commands.command()
async def get_just_victims(ctx):
    if ctx.author.id == ADMIN_ID:
        victims = Victims.retrieve_just_victims()
        await ctx.send(victims)
    else:
        await ctx.send('nice try pleb')


async def setup(bot):
    bot.add_command(bully)
    bot.add_command(liberate_victim)
    bot.add_command(add_reaction_role)
    bot.add_command(drop_reactionroles)
    bot.add_command(drop_victims)
    bot.add_command(read_reactionroles)
    bot.add_command(read_victims)
    bot.add_command(get_just_victims)