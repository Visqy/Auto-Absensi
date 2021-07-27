import discord
from discord.ext import commands

import json
from os.path import isfile
import sys

if not isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open('config.json') as file:
        config = json.load(file) 

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(ctx):
        return ctx.author.id in config["owner"]

    @commands.group(invoke_without_command=True, name='daftarnama', aliases=['dn'])
    @commands.check(is_owner)
    @commands.cooldown(rate=1, per=3)
    async def daftarnama(self, ctx):
        cur = self.bot.db.cursor()
        cur.execute("SELECT id, name, discord  FROM DAFTARNAMA  ORDER BY ID ASC")
        rows = cur.fetchall()
        embed = discord.Embed(
            title='Daftar Nama',
            colour=0x4C3CE7,
            description=''
        )
        for row in rows:
            embed.description +=f'''{row[0]}) {row[1].replace('^', "'")}    {row[2]}\n'''
        await ctx.send(embed=embed)

    @daftarnama.group()
    @commands.check(is_owner)
    @commands.cooldown(rate=1, per=3)
    async def update(self, ctx, id, dc):
        cur = self.bot.db.cursor()
        cur.execute(f"SELECT DISCORD FROM DAFTARNAMA WHERE ID = {int(id)}")
        row = cur.fetchall()
        cur.execute(f"UPDATE DAFTARNAMA SET DISCORD = '{dc}' WHERE ID = {int(id)}")
        self.bot.db.commit()
        embed = discord.Embed(
            title='Success',
            colour=0x4CE73C,
        )
        embed.set_thumbnail(url="https://i.ibb.co/Q9jNJkp/pngegg-1.png")
        embed.description = f"Changing {dc} from {(row[0])[0]} at {id}"
        await ctx.send(embed=embed)
    @daftarnama.error
    async def daftarnama_error(self, ctx, error):
        embed = discord.Embed(
            title='Error',
            color=0xE73C4C
        )
        embed.set_thumbnail(url='https://i.ibb.co/3MPVCV2/x.png')
        if isinstance(error, commands.CommandOnCooldown):
            embed.description = 'Sabar cok!'
        elif isinstance(error, commands.CheckFailure):
            embed.description = 'Lah lu sapa?'
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.description = 'Command kurang lengkap cuk.'
        else:
            embed.description = 'Gak tau kenapa.'
        await ctx.send(embed=embed, delete_after=3)
        await ctx.message.delete(delay=3)

def setup(bot):
    bot.add_cog(AdminCog(bot))