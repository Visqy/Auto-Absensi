import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name='h', aliases=['help'])
    async def h(self, ctx):
        embed=discord.Embed(colour=0x4C3CE7)
        embed.set_footer(text='Use ``*help <command>`` for more info on a command.')
        embed.set_author(name='Help Command', icon_url=ctx.bot.user.avatar_url) 
        embed.set_thumbnail(url="https://i.ibb.co/NK1SKkY/pngwing-com.png")
        embed.add_field(name='Everyone Command', value='``help``,``ping``',inline=False)
        embed.add_field(name='Absen Command', value='``absen``',inline=False)
        embed.add_field(name='Admin Command', value='``daftarnama``',inline=True)
        await ctx.send(embed=embed)

    @h.group()
    async def daftarnama(self, ctx):
        embed=discord.Embed(colour=0x4C3CE7)
        embed.set_author(name='Help Command : Daftar Nama', icon_url=ctx.bot.user.avatar_url) 
        embed.add_field(name='Aliases :', value='``dn``',inline=False)
        embed.add_field(name='Syntax :', value='``*daftarnama``\n``*daftarnama update <no> <discord id>``',inline=True)
        await ctx.send(embed=embed)

    @h.group()
    async def absen(self, ctx):
        embed=discord.Embed(colour=0x4C3CE7)
        embed.set_author(name='Help Command : Absen', icon_url=ctx.bot.user.avatar_url) 
        embed.add_field(name='Syntax :', value='``*absen [jenis kehadiran]``',inline=True)
        await ctx.send(embed=embed)

#    @h.group()
#    async def prefix(self, ctx):
#        embed=discord.Embed(title='Prefix', description='Set a new prefix', colour=0x4C3CE7)
#        embed.add_field(name='Syntax :', value='``prefix <new prefix>``')
#        await ctx.send(embed=embed)

    @h.group()
    async def ping(self, ctx):
        embed=discord.Embed(colour=0x00ff08)
        embed.set_author(name='Help Command : Ping', icon_url=ctx.bot.user.avatar_url)
        embed.add_field(name='Aliases :', value='``test``, ``p``',inline=False)
        embed.add_field(name='Syntax :', value='``*ping``',inline=True)
        await ctx.send(embed=embed)

    @h.group()
    async def help(self, ctx):
        embed=discord.Embed(colour=0x4C3CE7)
        embed.set_author(name='Help Command : Help', icon_url=ctx.bot.user.avatar_url)
        embed.add_field(name='Aliases :', value='``h``',inline=False)
        embed.add_field(name='Syntax :', value='``*help``',inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))