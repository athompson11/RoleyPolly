import discord
from discord.ext import commands, tasks
import emoji
import string

class PollCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Poll"])
    async def poll(self, ctx, *args):
        numoptions = len(args)-1
        usethumbs = False
        temp = list(args)
        description = ""
        reactions = []
        question = str(args[0])
        temp.pop(0)
        if numoptions <= 0:
            await ctx.send("I need options to list.")
            return
        if numoptions == 1:
            await ctx.send("We can't have a poll with one option, dummy.")
            return
        if numoptions == 2:
            usethumbs = True
        if usethumbs == True:
            description = ":thumbsup: {0}\n\n\n:thumbsdown: {1}".format(str(args[1]),str(args[2]))
            reactions = [":thumbsup:",":thumbsdown:"]
        else:
            for count,arg in enumerate(temp):
                reactions.append(":regional_indicator_symbol_letter_{0}:".format(string.ascii_lowercase[count]))
                description += ":regional_indicator_{1}: {0}\n\n".format(arg,string.ascii_lowercase[count])
        embed = discord.Embed(description=description)
        msg = await ctx.send("**{0}**".format(question,embed=embed)
        for emote in reactions:
            await msg.add_reaction(emoji.emojize(emote,use_aliases=True))
        return

def setup(bot):
    bot.add_cog(PollCommands(bot))

    
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