import random
from typing import Optional

import discord
import discord.ext.commands.context as context

from Methods import Emojis
from Objects import CustomViews, GameHolder
from Objects.Player import Player
from Tiles import Tile, TileList


async def send_tiles(player: Player):
    await player.user.send("Here are all your tiles:")
    player.tiles.sort()
    if len(player.shown_tiles.get_str_list())!=0: await player.user.send(Emojis.get_emojis(player.shown_tiles.get_str_list()))
    await player.user.send(Emojis.get_emojis(player.tiles.get_str_list()))


async def first_turn(interaction: Optional[discord.Interaction] = None, ctx: Optional[context.Context] = None) -> None:

    if ctx is None:
        if not interaction is None:
            ctx = await context.Context.from_interaction(interaction)
        else:
            raise Exception("both ctx and interaction arguments were None")

    random.shuffle(GameHolder.Game[ctx.guild].player_list)
    GameHolder.Game[ctx.guild].set_first_player()
    GameHolder.Game[ctx.guild].player_list.remove(GameHolder.Game[ctx.guild].first_player)
    GameHolder.Game[ctx.guild].player_list = [GameHolder.Game[ctx.guild].first_player] + GameHolder.Game[ctx.guild].player_list


    for player in GameHolder.Game[ctx.guild].player_list:
        for a in range(16):
            tile: Tile.Tile = GameHolder.Game[ctx.guild].draw_pile.draw()
            GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
            player.add_tile(tile)
        if player == GameHolder.Game[ctx.guild].first_player:
            tile: Tile.Tile = GameHolder.Game[ctx.guild].draw_pile.draw()
            GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
            player.add_tile(tile)
        player.tiles.sort()
        player.kong_check()

    feedback: str = ""

    for player in GameHolder.Game[ctx.guild].player_list:
        await player.user.send("The game has started")
        await send_tiles(player)
        if player.user.name == GameHolder.Game[ctx.guild].first_player.user.name:
            await player.user.send("your are the first player")

        feedback += "<@" + str(player.user.id) + "> "

    if interaction is None:
        await ctx.channel.send(feedback + "\nthe game has started,\n" + GameHolder.Game[ctx.guild].first_player.user.name + " is the first player")
    else:
        await interaction.followup.send(feedback + "\nthe game has started,\n" + GameHolder.Game[ctx.guild].first_player.user.name + " is the first player")

    is_winning_view: CustomViews.ChooseToWinView = CustomViews.ChooseToWinView(GameHolder.Game[ctx.guild].player_list[0].user)
    await GameHolder.Game[ctx.guild].player_list[0].user.send("Are you currently winning ?", view=is_winning_view)
    await is_winning_view.wait()

    if not is_winning_view.is_winning:

        throw_view = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].player_list[0])
        await GameHolder.Game[ctx.guild].player_list[0].user.send("Choose a tile to get rid of:", view=throw_view)
        await throw_view.wait()

        await ctx.channel.send("<@"+str(GameHolder.Game[ctx.guild].player_list[0].user.id)+"> thrown the tile:")
        await ctx.channel.send(Emojis.get_emoji(str(throw_view.thrown_tile)))
        await ctx.channel.send("Here are all the thrown tiles:")
        await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))

        for player in GameHolder.Game[ctx.guild].player_list:
            if player != GameHolder.Game[ctx.guild].player_list[0]:
                take_view: CustomViews.TakeView = CustomViews.TakeView(GameHolder.Game[ctx.guild].player_list[1].user.id == player.user.id,
                                                                       player, throw_view.thrown_tile, ctx)
                await player.user.send("Do you want to pickup this tile: "+str(Emojis.get_emoji(str(throw_view.thrown_tile)))+" ?", view=take_view)
                await take_view.wait()
                if not (take_view.result_combo is None):
                    player.combo_tiles = TileList.TileList(take_view.result_combo)
                    player.combo_type = take_view.result_combo_type
                else:
                    player.combo_tiles = None
                    player.combo_type = None
            else:
                player.combo_tiles = None
                player.combo_type = None
        priority: Optional[Player] = None
        for player in GameHolder.Game[ctx.guild].player_list:
            if not player.combo_type is None:
                if priority is None:
                    priority = player
                elif priority.combo_type.value < player.combo_type.value:
                    priority = player

        if not priority is None:
            GameHolder.Game[ctx.guild].throwed_tiles.takes_tile()
            combo_str = ""
            for tile in priority.combo_tiles: combo_str += Emojis.get_emoji(str(tile))
            await ctx.channel.send(f"{priority.user.name} picked up the tile, forming the combo {combo_str}")

            while GameHolder.Game[ctx.guild].player_list.index(priority) != 0:
                GameHolder.Game[ctx.guild].player_list = GameHolder.Game[ctx.guild].player_list[1:]+[GameHolder.Game[ctx.guild].player_list[0]]
            await taking_turn(priority, ctx)
        else:
            await ctx.channel.send("Nobody picked up this tile")

        await turn(GameHolder.Game[ctx.guild].player_list[1], ctx)
    else:
        await ctx.channel.send("<@"+str(GameHolder.Game[ctx.guild].player_list[0].user.id)+"> won !")
        await ctx.channel.send(Emojis.get_emojis(GameHolder.Game[ctx.guild].player_list[0].shown_tiles.get_str_list()))
        await ctx.channel.send(Emojis.get_emojis(GameHolder.Game[ctx.guild].player_list[0].tiles.get_str_list()))

async def turn(player: Player, ctx: context.Context) -> None:
    GameHolder.Game[ctx.guild].player_list = GameHolder.Game[ctx.guild].player_list[1:]+[GameHolder.Game[ctx.guild].player_list[0]]

    await ctx.send("It's now <@"+str(GameHolder.Game[ctx.guild].player_list[0].user.id)+">'s turn")

    drawn_tile = GameHolder.Game[ctx.guild].draw_pile.draw()
    GameHolder.Game[ctx.guild].draw_pile.remove_tile(drawn_tile)
    player.add_tile(drawn_tile)
    await player.user.send("You draw the tile: ")
    await player.user.send(Emojis.get_emoji(str(drawn_tile)))
    player.kong_check()

    await send_tiles(player)

    is_winning_view: CustomViews.ChooseToWinView = CustomViews.ChooseToWinView(GameHolder.Game[ctx.guild].player_list[0].user)
    await GameHolder.Game[ctx.guild].player_list[0].user.send("Are you currently winning ?", view=is_winning_view)
    await is_winning_view.wait()

    if not is_winning_view.is_winning:
        throw_view = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].player_list[0])
        await GameHolder.Game[ctx.guild].player_list[0].user.send("Choose a tile to get rid of:", view=throw_view)
        await throw_view.wait()

        await ctx.channel.send("<@" + str(GameHolder.Game[ctx.guild].player_list[0].user.id) + "> thrown the tile:")
        await ctx.channel.send(Emojis.get_emoji(str(throw_view.thrown_tile)))
        await ctx.channel.send("Here are all the thrown tiles:")
        await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))

        for player in GameHolder.Game[ctx.guild].player_list:
            if player != GameHolder.Game[ctx.guild].player_list[0]:
                take_view: CustomViews.TakeView = CustomViews.TakeView(
                    GameHolder.Game[ctx.guild].player_list[1].user.id == player.user.id,
                    player, throw_view.thrown_tile, ctx)
                await player.user.send(
                    "Do you want to pickup this tile: " + str(Emojis.get_emoji(str(throw_view.thrown_tile))) + " ?",
                    view=take_view)
                await take_view.wait()
                if not (take_view.result_combo is None):
                    player.combo_tiles = TileList.TileList(take_view.result_combo)
                    player.combo_type = take_view.result_combo_type
                else:
                    player.combo_tiles = None
                    player.combo_type = None
            else:
                player.combo_tiles = None
                player.combo_type = None
        priority: Optional[Player] = None
        for player in GameHolder.Game[ctx.guild].player_list:
            if not player.combo_type is None:
                if priority is None:
                    priority = player
                elif priority.combo_type.value < player.combo_type.value: priority = player

        if not priority is None:
            GameHolder.Game[ctx.guild].throwed_tiles.takes_tile()
            combo_str = ""
            for tile in priority.combo_tiles: combo_str += Emojis.get_emoji(str(tile))
            await ctx.channel.send(f"{priority.user.name} picked up the tile, forming the combo {combo_str}")

            while GameHolder.Game[ctx.guild].player_list.index(priority) != 0:
                GameHolder.Game[ctx.guild].player_list = GameHolder.Game[ctx.guild].player_list[1:] + [GameHolder.Game[ctx.guild].player_list[0]]
            await taking_turn(priority, ctx)
        else:
            await ctx.channel.send("Nobody picked up this tile")

        await turn(GameHolder.Game[ctx.guild].player_list[1], ctx)
    else:
        await ctx.channel.send("<@" + str(GameHolder.Game[ctx.guild].player_list[0].user.id) + "> won !")
        await ctx.channel.send(Emojis.get_emojis([str(tile) for tile in GameHolder.Game[ctx.guild].player_list[0].shown_tiles.tiles]))
        await ctx.channel.send(Emojis.get_emojis([str(tile) for tile in GameHolder.Game[ctx.guild].player_list[0].tiles.tiles]))

async def taking_turn(player: Player, ctx: context.Context) -> None:

    await ctx.send("It's now <@"+str(GameHolder.Game[ctx.guild].player_list[0].user.id)+">'s turn")

    await send_tiles(player)

    is_winning_view: CustomViews.ChooseToWinView = CustomViews.ChooseToWinView(GameHolder.Game[ctx.guild].player_list[0].user)
    await GameHolder.Game[ctx.guild].player_list[0].user.send("Are you currently winning ?", view=is_winning_view)
    await is_winning_view.wait()

    if not is_winning_view.is_winning:
        throw_view = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].player_list[0])
        await GameHolder.Game[ctx.guild].player_list[0].user.send("Choose a tile to get rid of:", view=throw_view)
        await throw_view.wait()

        await ctx.channel.send("<@" + str(GameHolder.Game[ctx.guild].player_list[0].user.id) + "> thrown the tile:")
        await ctx.channel.send(Emojis.get_emoji(str(throw_view.thrown_tile)))
        await ctx.channel.send("Here are all the thrown tiles:")
        await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))

        for player in GameHolder.Game[ctx.guild].player_list:
            if player != GameHolder.Game[ctx.guild].player_list[0]:
                take_view: CustomViews.TakeView = CustomViews.TakeView(
                    GameHolder.Game[ctx.guild].player_list[1].user.id == player.user.id,
                    player, throw_view.thrown_tile, ctx)
                await player.user.send(
                    "Do you want to pickup this tile: " + str(Emojis.get_emoji(str(throw_view.thrown_tile))) + " ?",
                    view=take_view)
                await take_view.wait()
                if not (take_view.result_combo is None):
                    player.combo_tiles = TileList.TileList(take_view.result_combo)
                    player.combo_type = take_view.result_combo_type
                else:
                    player.combo_tiles = None
                    player.combo_type = None
            else:
                player.combo_tiles = None
                player.combo_type = None
        priority: Optional[Player] = None
        for player in GameHolder.Game[ctx.guild].player_list:
            if not player.combo_type is None:
                if priority is None:
                    priority = player
                elif priority.combo_type.value < player.combo_type.value:
                    priority = player

        if not priority is None:
            GameHolder.Game[ctx.guild].throwed_tiles.takes_tile()
            combo_str = ""
            for tile in priority.combo_tiles: combo_str += Emojis.get_emoji(str(tile))
            await ctx.channel.send(f"{priority.user.name} picked up the tile, forming the combo {combo_str}")

            while GameHolder.Game[ctx.guild].player_list.index(priority) != 0:
                GameHolder.Game[ctx.guild].player_list = GameHolder.Game[ctx.guild].player_list[1:] + [
                    GameHolder.Game[ctx.guild].player_list[0]]
            await taking_turn(priority, ctx)
        else:
            await ctx.channel.send("Nobody picked up this tile")

        await turn(GameHolder.Game[ctx.guild].player_list[1], ctx)
    else:
        await ctx.channel.send("<@" + str(GameHolder.Game[ctx.guild].player_list[0].user.id) + "> won !")
        await ctx.channel.send(
            Emojis.get_emojis([str(tile) for tile in GameHolder.Game[ctx.guild].player_list[0].shown_tiles.tiles]))
        await ctx.channel.send(
            Emojis.get_emojis([str(tile) for tile in GameHolder.Game[ctx.guild].player_list[0].tiles.tiles]))