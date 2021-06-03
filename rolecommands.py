import discord
from discord.ext import commands, tasks
from discord.utils import get
import pickle
import emoji
import asyncio
import string

ServerConfigs = {} #Storage for the config settings for the various servers we're in (TODO, store in file)

class ServerConfig:
    OnJoinRoleID = 0
    WelcomeChannel = 0

class GroupConfig:
    Name = ""
    Explanation = ""
    Roles = []
    MessageID = 0
    EmojiMap = {}

class RoleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        #Check if user has admin role
        return ctx.author.guild_permissions.administrator

    @tasks.loop(minutes=15.0)
    async def SaveConfig(self):
        global ServerConfigs
        with open("ConfigDatabase.db","wb") as database:
            pickle.dump(ServerConfigs,database)
        return

    @commands.command()
    async def checkConfig(self,ctx):
        global ServerConfigs
        print(ServerConfigs[int(ctx.guild.id)].OnJoinRoleID)
        print(ServerConfigs[int(ctx.guild.id)].WelcomeChannel)

    @commands.command()
    async def SaveServerConfigs(self, ctx):
        global ServerConfigs
        with open("ConfigDatabase.db","wb") as database:
            pickle.dump(ServerConfigs,database)
        return
    
    @commands.command()
    async def SetOnJoinRole(self, ctx, myRole: discord.Role):
        try:
            ServerConfigs[int(ctx.guild.id)].OnJoinRoleID = int(myRole.id)
            await ctx.send("Role set to role id # {0}".format(ServerConfigs[int(ctx.guild.id)].OnJoinRoleID))
            return
        except:
            ServerConfigs[int(ctx.guild.id)] = ServerConfig()
            ServerConfigs[int(ctx.guild.id)].OnJoinRoleID = int(myRole.id)
            await ctx.send("Role set to role id # {0}".format(ServerConfigs[int(ctx.guild.id)].OnJoinRoleID))
            return

    @commands.command()
    async def SetWelcomeChannel(self, ctx, myChannel: discord.TextChannel):
        try:
            ServerConfigs[int(ctx.guild.id)].WelcomeChannel = int(myChannel.id)
            await ctx.send("Channel set to channel id # {0}".format(ServerConfigs[int(ctx.guild.id)].WelcomeChannel))
            return
        except:
            ServerConfigs[int(ctx.guild.id)] = ServerConfig()
            ServerConfigs[int(ctx.guild.id)].WelcomeChannel = int(myChannel.id)
            await ctx.send("Channel set to channel id # {0}".format(ServerConfigs[int(ctx.guild.id)].WelcomeChannel))
            return
            

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(ServerConfigs[int(member.guild.id)].WelcomeChannel)
        print(channel)
        if channel is not None:
            await channel.send('WELCOME NEW FRIEND!!! {0.mention}'.format(member))
        if ServerConfigs[member.guild.id].OnJoinRoleID != 0:
            print("Got role")
            server = member.guild
            role = discord.utils.get(server.roles, id=ServerConfigs[member.guild.id].OnJoinRoleID)
            await member.add_roles(role)
            return
def setup(bot):
    global ServerConfigs
    try:
        with open("ConfigDatabase.db","rb") as database:
            ServerConfigs = pickle.load(database)
    except:
        print("Couldn't find database!")
        pass
    bot.add_cog(RoleCommands(bot))