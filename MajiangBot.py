from types import NoneType

import discord
from discord.ext import commands
from random import choice

from DrawPile import DrawPile
from Player import Player
from Tile import Tile

prefix_file = open("prefix.txt")
prefix_line = prefix_file.readline()
prefix = prefix_line[-1]
prefix_file.close()

token_file = open("token.txt")
token = token_file.read()
token_file.close()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

starting = {}
Players = {}
First_player = {}
draw_pile = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot connected as {0.user} !".format(bot))

@bot.tree.command(name = "emoji",
              description = "send the corresponding majiang emoji (for test purposes)")
async def emoji(interaction, name: str):
    await interaction.response.send_message(str(discord.utils.get(bot.emojis, name=name)))

@bot.command()
async def emoji(ctx, name: str):
    await ctx.send(str(discord.utils.get(bot.emojis, name=name)))

@bot.tree.command(name = "start",
                  description = "Starts a majiang game, type 'join' to join it. Use this command again to force start the game")
async def start(interaction):
    global starting
    global Players

    if not interaction.guild in starting:
        starting.update({interaction.guild: False})
    if not interaction.guild in Players:
        Players.update({interaction.guild: []})

    if starting[interaction.guild] and len(Players) > 0:
        starting.update({interaction.guild: False})

        draw_pile.update({interaction.guild: DrawPile()})
        player: Player = choice(Players[interaction.guild])
        First_player.update({interaction.guild: player.user.name})
        Players[interaction.guild].remove(player)
        player_list = [player]
        for player in Players[interaction.guild]:
            player_list.append(player)

        Players[interaction.guild] = player_list

        for player in Players[interaction.guild]:
            for a in range(16):
                tile: Tile = draw_pile[interaction.guild].draw()
                draw_pile[interaction.guild].remove_tile(tile)
                player.add_tile(tile)
            if player.user.name == First_player[interaction.guild]:
                tile: Tile = draw_pile[interaction.guild].draw()
                draw_pile[interaction.guild].remove_tile(tile)
                player.add_tile(tile)
            player.tiles.sort()

        feedback: str = ""

        for player in Players[interaction.guild]:
            text = ""
            for tile in player.tiles.tiles:
                text += str(discord.utils.get(bot.emojis, name=str(tile)))
            await player.user.send("here's your tiles:\n"+text)
            if player.user.name == First_player[interaction.guild]:
                await player.user.send("your are the first player")

            feedback += "<@"+str(player.user.id)+">"

        await interaction.response.send_message(feedback+"\nthe game has started,\n"+First_player[interaction.guild]+" is the first player")

    else:
        Players[interaction.guild] = []
        starting[interaction.guild] = True
        await interaction.response.send_message("starting game,\ntype \"join\" to join the game:")

@bot.command()
async def start(ctx):
    global starting
    global Players

    if not ctx.guild in starting:
        starting.update({ctx.guild: False})
    if not ctx.guild in Players:
        Players.update({ctx.guild: []})

    if starting[ctx.guild] and len(Players) > 0:
        starting.update({ctx.guild: False})

        draw_pile.update({ctx.guild: DrawPile()})
        player: Player = choice(Players[ctx.guild])
        First_player.update({ctx.guild: player.user.name})
        Players[ctx.guild].remove(player)
        player_list = [player]
        for player in Players[ctx.guild]:
            player_list.append(player)

        Players[ctx.guild] = player_list

        for player in Players[ctx.guild]:
            for a in range(16):
                tile: Tile = draw_pile[ctx.guild].draw()
                draw_pile[ctx.guild].remove_tile(tile)
                player.add_tile(tile)
            if player.user.name == First_player[ctx.guild]:
                tile: Tile = draw_pile[ctx.guild].draw()
                draw_pile[ctx.guild].remove_tile(tile)
                player.add_tile(tile)
            player.tiles.sort()

        feedback: str = ""

        for player in Players[ctx.guild]:
            text = ""
            for tile in player.tiles.tiles:
                emoji_text = str(discord.utils.get(bot.emojis, name=str(tile)))
                if emoji_text == "None":
                    emoji_text = str(tile)
                text += emoji_text
            await player.user.send("here's your tiles:\n"+text)
            if player.user.name == First_player[ctx.guild]:
                await player.user.send("your are the first player")

            feedback += "<@"+str(player.user.id)+">"

        await ctx.send(feedback+"\nthe game has started,\n"+First_player[ctx.guild]+" is the first player")

    else:
        Players[ctx.guild] = []
        starting[ctx.guild] = True
        await ctx.send("starting game,\ntype \"join\" to join the game:")


@bot.event
async def on_message(message):
    global starting
    global Players

    if not message.guild in starting:
        starting.update({message.guild: False})
    if not message.guild in Players:
        Players.update({message.guild: []})

    if message.content[0] != bot.command_prefix:
        if not message.author.bot:
            if starting[message.guild]:
                if message.content == "join":
                    if not Player(message.author) in Players[message.guild]:
                        Players[message.guild].append(Player(message.author))
                        await message.channel.send(message.author.name+" successfully registered")
                        if len(Players[message.guild]) == 4:
                            await message.channel.send("type \"!start\" to start the game")
                    else:
                        await message.channel.send("your are already in !")
    else:
        await bot.process_commands(message)

print("launch the bot ?")
must_start: str = input()
if must_start in ["y", "yes", "1"]:
    print("prefix="+prefix)
    bot.run(token)