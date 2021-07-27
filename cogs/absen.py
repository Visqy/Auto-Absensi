import discord
from discord.ext import commands

import datetime
import asyncio
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exceptions

#form automation
async def script(content):
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    date= datetime.datetime.strptime(content[2], '%m/%d/%y %H:%M:%S')
    days={'Mon':'Senin', 'Tue':'Selasa', 'Wed':'Rabu', 'Thu':'Kamis', 'Fri':'Jumat', 'Sat':'Sabtu'}
    driver.get(os.getenv("LINK_GFORM").format(content[1].replace(' ','+'),'1143179380' if content[1]=='XII IPA 1' else '1955799690', content[0].replace(' ','+').replace('^', "'"), content[3], date.strftime('%Y-%m-%d'), days[date.strftime('%a')], date.strftime('%H:%M')))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div/div/div"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div/div/div[2]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div/div/div[2]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div/div/div[2]"))).click()
    driver.quit()

class Absen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=3)
    async def absen(self, ctx, p='datang'):
        prep = ['datang','pulang']
        if p in prep:
            author = ctx.message.author
            cur = self.bot.db.cursor()
            time = datetime.datetime.now()
            embed = discord.Embed(
                title = 'Confirmation',
                colour=0x4C3CE7
            )
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            cur.execute(f"SELECT name,class,discord FROM DN WHERE discord = '{author.id}'")
            data = cur.fetchall()
            embed.description = f'''Nama : {(data[0])[0].replace('^', "'")}\nKelas : {(data[0])[1]}\nWaktu : {time.strftime('%A, %d %B %Y %H:%M')}\nPresensi : {p.capitalize()}'''
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
                            title = 'Processing...',
                            colour=0x4CE73C
                        )
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        await script([f'{(data[0])[0]}', f'{(data[0])[1]}', f"{time.strftime('%m/%d/%y %H:%M:%S')}", f'{p.capitalize()}'])
                        embed = discord.Embed(
                            title = 'Success',
                            colour=0x4CE73C
                        )
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        embed.set_thumbnail(url="https://i.ibb.co/Q9jNJkp/pngegg-1.png")
                        await message.edit(embed=embed)
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
