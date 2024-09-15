import discord
from discord.ext import commands

prefix_file = open("Constants/prefix.txt")
prefix_line = prefix_file.readline()
prefix = prefix_line[-1]
prefix_file.close()

token_file = open("Constants/token.txt")
token = token_file.read()
token_file.close()

ids_file = open("Constants/admins.txt")
admin_ids = ids_file.read().split(",")
ids_file.close()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)