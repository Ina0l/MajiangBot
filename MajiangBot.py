import discord

from discord.ext.commands import Context

import Bot
import TurnsAlogrithms
import Objects.GameHolder as GameHolder
from Objects.Player import Player
from Tiles.Tile import Tile


bot = Bot.bot

starting: dict[discord.Guild: bool] = {}
In_Game: dict[discord.Guild: bool] = {}


def launch_bot():
    Bot.bot.run(Bot.token)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot connected as {0.user} !".format(bot))

@bot.tree.command(name = "start",
                  description = "Starts a majiang game, type 'join' to join it. Use this command again to force start the game")
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

        if starting[interaction.guild] and len(GameHolder.Game[interaction.guild].player_list) > 0:
            starting.update({interaction.guild: False})
            In_Game.update({interaction.guild: True})

            GameHolder.Game[interaction.guild].set_first_player()
            GameHolder.Game[interaction.guild].player_list.remove(GameHolder.Game[interaction.guild].first_player)
            player_list = [GameHolder.Game[interaction.guild].first_player]
            for player in GameHolder.Game[interaction.guild].player_list:
                player_list.append(player)

            GameHolder.Game[interaction.guild].player_list = player_list

            for player in GameHolder.Game[interaction.guild].player_list:
                for a in range(16):
                    tile: Tile = GameHolder.Game[interaction.guild].draw_pile.draw()
                    GameHolder.Game[interaction.guild].draw_pile.remove_tile(tile)
                    player.add_tile(tile)
                if player == GameHolder.Game[interaction.guild].first_player:
                    tile: Tile = GameHolder.Game[interaction.guild].draw_pile.draw()
                    GameHolder.Game[interaction.guild].draw_pile.remove_tile(tile)
                    player.add_tile(tile)
                player.tiles.sort()

            feedback: str = ""

            for player in GameHolder.Game[interaction.guild].player_list:
                text = ""
                for tile in player.tiles.tiles:
                    text += str(discord.utils.get(bot.emojis, name=str(tile)))
                await player.user.send("here's your tiles:\n"+text)
                if player.user.name == GameHolder.Game[interaction.guild].first_player.user.name:
                    await player.user.send("your are the first player")

                feedback += "<@"+str(player.user.id)+">"

            await interaction.response.send_message(feedback +"\nthe game has started,\n" +
                                                    GameHolder.Game[interaction.guild].first_player.user.name + " is the first player")

            await TurnsAlogrithms.first_turn(interaction=interaction)


        else:
            GameHolder.Game[interaction.guild] = GameHolder.GameHolder()
            starting[interaction.guild] = True
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

        if starting[ctx.guild] and len(GameHolder.Game[ctx.guild].player_list) > 0:
            starting.update({ctx.guild: False})
            In_Game.update({ctx.guild: True})

            GameHolder.Game[ctx.guild].set_first_player()
            GameHolder.Game[ctx.guild].player_list.remove(GameHolder.Game[ctx.guild].first_player)
            player_list = [GameHolder.Game[ctx.guild].first_player]
            for player in GameHolder.Game[ctx.guild].player_list:
                player_list.append(player)

            GameHolder.Game[ctx.guild].player_list = player_list

            for player in GameHolder.Game[ctx.guild].player_list:
                for a in range(16):
                    tile: Tile = GameHolder.Game[ctx.guild].draw_pile.draw()
                    GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
                    player.add_tile(tile)
                if player == GameHolder.Game[ctx.guild].first_player:
                    tile: Tile = GameHolder.Game[ctx.guild].draw_pile.draw()
                    GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
                    player.add_tile(tile)
                player.tiles.sort()

            feedback: str = ""

            for player in GameHolder.Game[ctx.guild].player_list:
                text = ""
                for tile in player.tiles.tiles:
                    text += str(discord.utils.get(bot.emojis, name=str(tile)))
                await player.user.send("here's your tiles:\n" + text)
                if player.user.name == GameHolder.Game[ctx.guild].first_player.user.name:
                    await player.user.send("your are the first player")

                feedback += "<@" + str(player.user.id) + ">"

            await ctx.send(feedback + "\nthe game has started,\n" + GameHolder.Game[ctx.guild].first_player.user.name + " is the first player")

            await TurnsAlogrithms.first_turn(ctx=ctx)

        else:
            GameHolder.Game[ctx.guild] = GameHolder.GameHolder()
            starting[ctx.guild] = True
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
                    if not Player(message.author) in GameHolder.Game[message.guild].player_list:
                        GameHolder.Game[message.guild].player_list.append(Player(message.author))
                        await message.channel.send(message.author.name+" successfully registered")
                        if len(GameHolder.Game[message.guild].player_list) == 4:
                            await message.channel.send("type \"!start\" to start the game")
                    else:
                        await message.channel.send("your are already in !")
    else:
        await bot.process_commands(message)