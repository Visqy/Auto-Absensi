import discord
from discord.ext import commands
import datetime
import asyncio


class Absen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=3)
    async def absen(self, ctx, p='hadir'):
        prep = ['hadir','izin','sakit']
        if p in prep:
            author = ctx.message.author
            cur = self.bot.db.cursor()
            time = datetime.datetime.now()
            embed = discord.Embed(
                title = 'Confirmation',
                colour=0x4C3CE7
            )
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            cur.execute(f"SELECT name,class,discord FROM DAFTARNAMA WHERE discord = '{author.id}'")
            data = cur.fetchall()
            embed.description = f"Nama : {(data[0])[0]}\nKelas : {(data[0])[1]}\nWaktu : {time.strftime('%A, %d %B %Y %H:%M')}\nPresensi : {p.capitalize()}"
            message = await ctx.send(embed=embed)
            #Reaction code
            await message.add_reaction('☑️')
            await message.add_reaction('❌')
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['❌','☑️']
            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=check)
                    if str(reaction.emoji) == "☑️":
                        embed = discord.Embed(
                            title = 'Success',
                            colour=0x4CE73C
                        )
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        embed.set_thumbnail(url="https://i.ibb.co/Q9jNJkp/pngegg-1.png")
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        break
                    elif str(reaction.emoji) == "❌":
                        await message.delete()
                        break
                    else:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    await message.delete()
                    break
        else:
            embed = discord.Embed(
                title = 'Error',
                colour=0xE73C4C,
                description='Salah Presensinya cok'
            )
            embed.set_thumbnail(url='https://i.ibb.co/3MPVCV2/x.png')
            await ctx.send(embed=embed)
    @absen.error
    async def absen_error(self, ctx, error):
        embed = discord.Embed(
            title='Error',
            color=0xE73C4C
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url='https://i.ibb.co/3MPVCV2/x.png')
        if isinstance(error, commands.CommandOnCooldown):
            embed.description = 'Sabar cok!'
        elif isinstance(error, commands.CommandInvokeError):
            embed.description = 'ID discord anda tidak terdaftar dalam sistem.'
        else:
            embed.description = 'Gak tau kenapa.'
            raise error
        await ctx.send(embed=embed, delete_after=5)
        await ctx.message.delete(delay=5)
        

def setup(bot):
    bot.add_cog(Absen(bot))