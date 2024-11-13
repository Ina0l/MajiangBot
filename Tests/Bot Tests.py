import discord
from discord.ext import commands

prefix = "!"

#TODO: remove this before every commit and push
token = ""

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.command()
async def test(ctx):
    await ctx.send("")

bot.run(token)