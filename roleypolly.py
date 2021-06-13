import discord
from discord.ext import commands, tasks
import configparser

intents = discord.Intents.default()
intents.members = True
token = None
owner = None

bot = commands.Bot(command_prefix="!r",intents=intents) #The command prefix, we could technically let this be configurable
config = configparser.ConfigParser()
read = config.read('config.ini') #returns a list of files successfully read
if not read:
    quit()
else:
    token = config["Token"]
    owner = config["Owner"]


def is_owner(): #A function that checks if the person running the command is me
    async def predicate(ctx):
        global owner
        return ctx.author.id == owner
    return commands.check(predicate)

def is_owner(): #A function that checks if the person running the command is the server owner
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner.id
    return commands.check(predicate)

@bot.command()
@is_owner() #Live modify the code they said, it'd be fun they said
async def reload(ctx):
    bot.reload_extension('pollcommands')
    bot.reload_extension('rolecommands')
    return
    
"""@bot.command()
@is_owner() #Todo: Work on this to allow other roles to customize role menus
async def enableroleconfig(ctx,*,role: discord.Role = None,config: bool):
    global ServerConfigs
    if ctx.guild.id not in ServerConfigs:
        ServerConfigs.append(str(ctx.guild.id))
    if 
"""    

"""
@bot.event
async def on_command_error(ctx, error): #Handle command not found errors cleanly
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return
"""
@bot.event
async def on_ready():
    print("Logged on as {0}!".format(bot.user))
    bot.load_extension('pollcommands')
    bot.load_extension('rolecommands')

bot.run(token)