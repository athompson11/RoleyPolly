import discord
from discord.ext import commands, tasks
from discord.utils import get
import pickle
import emoji
import asyncio
import string

ServerConfigs = {} #Storage for the config settings for the various servers we're in (TODO, store in file)

class ServerConfig:
    RoleGroups = {}

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
    async def SaveServerConfigs(self, ctx):
        global ServerConfigs
        with open("ConfigDatabase.db","wb") as database:
            pickle.dump(ServerConfigs,database)
        return

    @commands.command()
    async def SetupServer(self, ctx):
        await ctx.send("Get started by creating a role group with by using !CreateGroup \"name\", and then add a few roles to it with !AddRole \"groupname\" \"rolenames\" and finally make a role menu with !RoleMenu \"groupname!\"")
        global ServerConfigs
        if str(ctx.guild.id) in ServerConfigs:
            await ctx.send("But you already knew that, silly goose.")
        else:
            config = ServerConfig()
            ServerConfigs.update({str(ctx.guild.id):config})
            await ctx.invoke(self.bot.get_command('SaveServerConfigs'))
            return
    @commands.command()
    async def CreateGroup(self, ctx, *, GroupName: str):
        global ServerConfigs
        try:
            groupconfig = GroupConfig()
            groupconfig.Name = GroupName
            serverconfig = ServerConfigs[str(ctx.guild.id)]
            serverconfig.RoleGroups.update({groupconfig.Name:groupconfig})
            await ctx.send("Group successfully created!")
            return
        except:
            await ctx.send("Abbie messed up somewhere. :(")
        
    @commands.command()
    async def AddRoles(self, ctx, *args):
        global ServerConfigs
        temp = list(args) #Temp storage for the arguments provided
        group = str(args[0]) #What the Group's name is
        temp.pop(0) #Remove the Group from the list of roles provided
        roleids=[]
        GroupObject = GroupConfig()
        ServerObject = ServerConfig()
        ServerObject = ServerConfigs[str(ctx.guild.id)]
        GroupObject = ServerObject.RoleGroups[group]
        for role in temp:
            roleobject = get(ctx.guild.roles, name=role)
            roleids.append(roleobject.id)
        GroupObject.Roles.append(roleids)
        return
    
    @commands.command()
    async def CreateRoleMenu(self, ctx, *, GroupName: str):
        description = ""
        reactions = []
        ServerObject = ServerConfig()
        GroupObject = GroupConfig()
        ServerObject = ServerConfigs[str(ctx.guild.id)]
        GroupObject = ServerObject.RoleGroups[GroupName]
        for count,arg in enumerate(GroupObject.Roles): #From A-Z, just like the poll, I doubt we'd have use cases where we need more than 20 or so options
                reactions.append(":regional_indicator_symbol_letter_{0}:".format(string.ascii_lowercase[count]))
                description += ":regional_indicator_{1}: {0}\n\n".format(arg,string.ascii_lowercase[count]) #Todo: Fetch role name from ID
                GroupObject.EmojiMap.update({":regional_indicator_symbol_letter_{0}:".format(string.ascii_lowercase[count]):arg})
        embed = discord.Embed(description=description)
        msg = await ctx.send(embed=embed) #Send it
        for emote in reactions:
            await msg.add_reaction(emoji.emojize(emote,use_aliases=True)) #React to the message we just sent
        GroupObject.MessageID = msg.id
        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global ServerConfigs
        print(payload.user_id)
        print(self.bot.user.id)
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.guild_id) in ServerConfigs:
            ServerObject = ServerConfig()
            ServerObject = ServerConfigs[str(payload.guild_id)]
            GroupObject = GroupConfig()
            foundGroup = False
            for group in ServerObject.RoleGroups.keys():
                if int(payload.message_id) == GroupObject.MessageID:
                    GroupObject = ServerObject.RoleGroups[group]
                    foundGroup = True
                    break
            if foundGroup:
                print("Found group, could have added role.")
            else:
                print("Can't find group.")
            return


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global ServerConfigs
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.guild_id) in ServerConfigs:
            ServerObject = ServerConfig()
            ServerObject = ServerConfigs[str(payload.guild_id)]
            GroupObject = GroupConfig()
            foundGroup = False
            for group in ServerObject.RoleGroups.keys():
                if int(payload.message_id) == GroupObject.MessageID:
                    GroupObject = ServerObject.RoleGroups[group]
                    foundGroup = True
                    break
            if foundGroup:
                print("Found group, could have removed role.")
            else:
                print("Can't find group.")
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


    
"""    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

  @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """"""Says hello""""""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member
"""