import discord
from discord.ext import commands, tasks
import string

class PollCommands(commands.Cog): #Class that contains this 'category' of commands
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["Poll"])
    async def poll(self, ctx, *args):
        numoptions = len(args)-1 #By default we're provided the command as well, so we have to knock one off
        usethumbs = False #Whether or not we're going to only have two arguments
        temp = list(args) #Temp storage for the arguments provided
        description = "" #Description for the embed
        reactions = [] #The reactions we're using
        #question = str(args[0]) #What the question specifically is
        temp.pop(0) #Remove the question from the list of arguments provided
        if numoptions <= 0: #We need things to list
            await ctx.send("I need options to list.") 
            return
        elif numoptions == 1: #Not a poll without options
            await ctx.send("We can't have a poll with one option, dummy.")
            return
        elif numoptions == 2: #Only two options provided, +1 and -1 are best
            usethumbs = True
        if usethumbs == True:
            description = ":thumbsup: {0}\n\n\n:thumbsdown: {1}".format(str(args[1]),str(args[2]))
            reactions = [":thumbsup:",":thumbsdown:"]
        else:
            for count,arg in enumerate(temp): #From A-Z, I doubt we'd have use cases where we need more than 20 or so options
                reactions.append(":regional_indicator_{0}:".format(string.ascii_lowercase[count]))
                description += ":regional_indicator_{0}: {1}\n\n".format(string.ascii_lowercase[count],arg)
        embed = discord.Embed(description=description)
        print(description)
        embed = discord.Embed(description=description)
        msg = await ctx.send("**{0}**".format(str(args[0])),embed=embed)
        for emote in reactions:
            await msg.add_reaction(emote)
        return

def setup(bot):
    bot.add_cog(PollCommands(bot)) #Add the category to the bot

# Reference functions for how to implement a base listener and command
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