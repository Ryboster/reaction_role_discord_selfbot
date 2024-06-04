# bot.py
### External Modules
import sys # For interacting with the operating system
import asyncio # For asynchronous operations
import json # For reading config file

### Discord Modules
sys.path.insert(0, 'discord.py-self')
from discord.ext import commands

# Own modules
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

    
from bot_commands import *
from bot_events import Events


async def main():
    #await bot.load_extension('bot_events')
    await bot.add_cog(Events(bot))
    await bot.load_extension('bot_commands')
    await bot.start(token)
    
try:
    asyncio.run(main())
except KeyboardInterrupt:
    asyncio.run(bot.close())