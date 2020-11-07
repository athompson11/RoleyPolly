import discord
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix="!")
with open("token.cfg") as tokenconfig:
    Token = tokenconfig.readline()

def is_abbie():
    async def predicate(ctx):
        return ctx.author.id == 210279390288805888
    return commands.check(predicate)

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner.id
    return commands.check(predicate)

@bot.command()
@is_abbie()
async def reload(ctx):
    bot.reload_extension('pollcommands')
    bot.reload_extension('rolecommands')
    return
    
@bot.command()
@is_owner()
async def enableroleconfig(ctx,*,role: discord.Role = None,config: bool):
    return


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return

@bot.event
async def on_ready():
    print("Logged on as {0}!".format(bot.user))
    bot.load_extension('pollcommands')
    bot.load_extension('rolecommands')

bot.run(Token)