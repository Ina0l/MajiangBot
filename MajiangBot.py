import discord

from discord.ext.commands import Context

import Bot
import TurnsAlogrithms
import Objects.GameHolder as GameHolder
from Objects.Player import Player


bot = Bot.bot

starting: dict[discord.Guild: bool] = {}
In_Game: dict[discord.Guild: bool] = {}


def launch_bot(): bot.run(Bot.token)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot connected as {0.user} !".format(bot))

@bot.tree.command(name = "start",
                  description = "Starts a majiang game, type 'join' to join it. Use this command again to start the game")
async def start(interaction):
    global starting
    global In_Game

    if not interaction.guild in In_Game:
        In_Game.update({interaction.guild: False})
    if not interaction.guild in GameHolder.Game:
        GameHolder.Game.update({interaction.guild: GameHolder.GameHolder()})

    if not In_Game[interaction.guild]:
        if not interaction.guild in starting:
            starting.update({interaction.guild: False})

        if starting[interaction.guild]:
            if len(GameHolder.Game[interaction.guild].player_list) > 0:
                starting.update({interaction.guild: False})
                In_Game.update({interaction.guild: True})

                await TurnsAlogrithms.first_turn(interaction=interaction)
            else: await interaction.response.send_message("You need at least 2 players to player majiang")

        else:
            GameHolder.Game[interaction.guild] = GameHolder.GameHolder()
            starting[interaction.guild] = True
            GameHolder.Game[interaction.guild].player_list.append(Player(interaction.user))
            await interaction.response.send_message("starting game,\ntype \"join\" to join the game:")
    else:
        await interaction.response.send_message("A game is already in progress")

@bot.command()
async def start(ctx: Context):
    global starting
    global In_Game

    if not ctx.guild in In_Game:
        In_Game.update({ctx.guild: False})
    if not ctx.guild in GameHolder.Game:
        GameHolder.Game.update({ctx.guild: GameHolder.GameHolder()})

    if not In_Game[ctx.guild]:
        if not ctx.guild in starting:
            starting.update({ctx.guild: False})

        if starting[ctx.guild]:
            if len(GameHolder.Game[ctx.guild].player_list) > 0:
                starting.update({ctx.guild: False})
                In_Game.update({ctx.guild: True})

                await TurnsAlogrithms.first_turn(ctx=ctx)
            else: await ctx.send("You need at least 2 players to play majiang")

        else:
            GameHolder.Game[ctx.guild] = GameHolder.GameHolder()
            starting[ctx.guild] = True
            GameHolder.Game[ctx.guild].player_list.append(Player(ctx.message.author))
            await ctx.send("starting game,\ntype \"join\" to join the game:")
    else:
        await ctx.send("A game is already in progress")


@bot.event
async def on_message(message):
    global starting

    if not message.guild in starting:
        starting.update({message.guild: False})

    if message.content == "":
        return

    if message.content[0] != bot.command_prefix:
        if not message.author.bot:
            if starting[message.guild]:
                if message.content == "join":
                    is_user_registered = False
                    for player in GameHolder.Game[message.guild].player_list:
                        if player.user.id == message.author.id:
                            is_user_registered = True
                    if not is_user_registered:
                        if len(GameHolder.Game[message.guild].player_list) != 4:
                            GameHolder.Game[message.guild].player_list.append(Player(message.author))
                            await message.channel.send(message.author.name+" successfully registered")
                            if len(GameHolder.Game[message.guild].player_list) == 4:
                                await message.channel.send("type \"!start\" to start the game")
                        else: await message.channel.send("there are already 4 players registered")
                    else:
                        await message.channel.send("your are already in !")
    else:
        await bot.process_commands(message)