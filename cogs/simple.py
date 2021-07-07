import discord
from discord.ext import commands

class SimpleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.command()
    #async def prefix(ctx, prefix):
    #    with open(r"..\prefixes.json", 'r') as f:
    #        prefixes=json.load(f)
    #    prefixes[(ctx.guild.id)]=prefix
    #    with open(r"..\prefixes.json", 'w') as f:
    #        json.dump(prefixes, f, indent=-4)
    #    await ctx.send(f'The prefix was changed to {prefix}')

    @commands.command(name='ping', aliases=['test', 'p'])
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}ms')

def setup(bot):
    bot.add_cog(SimpleCog(bot))