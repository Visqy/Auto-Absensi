import discord
from discord.ext import commands

import os
from os.path import isfile, join

import sys, traceback

import psycopg2
import asyncio
import json

if not isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open('config.json') as file:
        config = json.load(file) 

bot = commands.Bot(command_prefix=config['prefix'], help_command=None)
cogs_dir='cogs'

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Testing', type=1))
    print(f'Started')

async def initialize():
    await bot.wait_until_ready()
    bot.db = psycopg2.connect(host= os.getenv("HOST_DB"),
                    port= "5432",
                    database= os.getenv("DB"), 
                        user = os.getenv("USER_DB"), 
                     password = os.getenv("PASS_DB"))

bot.loop.create_task(initialize())

bot.run(os.getenv("DISCORD_TOKEN"))
asyncio.run(bot.db.close())