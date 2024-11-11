import discord
import discord.ext.commands.context as context

import Bot
from Methods import Emojis
from Objects import CustomViews, GameHolder
from Objects.Player import Player
from Tiles import Tile


async def first_turn(interaction: discord.Interaction = None, ctx: context.Context = None) -> None:

    if ctx is None:
        if not interaction is None:
            ctx = await context.Context.from_interaction(interaction)
        else:
            raise Exception("both ctx and interaction arguments were None")

    GameHolder.Game[ctx.guild].set_first_player()
    GameHolder.Game[ctx.guild].player_list.remove(GameHolder.Game[ctx.guild].first_player)
    player_list = [GameHolder.Game[ctx.guild].first_player]
    for player in GameHolder.Game[ctx.guild].player_list:
        player_list.append(player)

    GameHolder.Game[ctx.guild].player_list = player_list

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

    feedback: str = ""

    for player in GameHolder.Game[ctx.guild].player_list:
        text = ""
        for tile in player.tiles.tiles:
            text += str(discord.utils.get(Bot.bot.emojis, name=str(tile)))
        await player.user.send("here's your tiles:\n" + text)
        if player.user.name == GameHolder.Game[ctx.guild].first_player.user.name:
            await player.user.send("your are the first player")

        feedback += "<@" + str(player.user.id) + ">"

    await ctx.send(feedback + "\nthe game has started,\n" + GameHolder.Game[
        ctx.guild].first_player.user.name + " is the first player")


    is_winning_view: CustomViews.ChooseToWinView = CustomViews.ChooseToWinView(GameHolder.Game[ctx.guild].first_player.user)
    await GameHolder.Game[ctx.guild].first_player.user.send("Are you currently winning ?", view=is_winning_view)
    await is_winning_view.wait()

    if not is_winning_view.is_winning:

        throw_view = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].first_player)
        await GameHolder.Game[ctx.guild].first_player.user.send("Choose a tile to get rid of:", view=throw_view)
        await throw_view.wait()

        await ctx.channel.send("<@"+str(GameHolder.Game[ctx.guild].first_player.user.id)+"> thrown the tile:")
        await ctx.channel.send(Emojis.get_emoji(str(throw_view.thrown_tile)))
        await ctx.channel.send("Here are all the thrown tiles:")
        await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))

        take_view: CustomViews.TakeView = CustomViews.TakeView(GameHolder.Game[ctx.guild].player_list[1], throw_view.thrown_tile)
        await ctx.send("Do you want to pickup this tile ?", view=take_view)

        await turn(GameHolder.Game[ctx.guild].player_list[1], ctx)
    else:
        await ctx.channel.send("<@"+str(GameHolder.Game[ctx.guild].first_player.user.id)+"> won !")
        await ctx.channel.send(Emojis.get_emojis(GameHolder.Game[ctx.guild].first_player.shown_tiles.get_str_list()))
        await ctx.channel.send(Emojis.get_emojis(GameHolder.Game[ctx.guild].first_player.tiles.get_str_list()))

async def turn(player: Player, ctx: context.Context) -> None:
    drawn_tile = GameHolder.Game[ctx.guild].draw_pile.draw()
    GameHolder.Game[ctx.guild].draw_pile.remove_tile(drawn_tile)
    player.add_tile(drawn_tile)

    await player.user.send("You drawn the tile:")
    await player.user.send(Emojis.get_emoji(str(drawn_tile)))
    await player.user.send("Here are all your tiles:")
    player.tiles.sort()
    await player.user.send(Emojis.get_emojis(player.shown_tiles.get_str_list()))
    await player.user.send(Emojis.get_emojis(player.tiles.get_str_list()))

    is_winning_view: CustomViews.ChooseToWinView = CustomViews.ChooseToWinView(GameHolder.Game[ctx.guild].first_player.user)
    await GameHolder.Game[ctx.guild].first_player.user.send("Are you currently winning ?", view=is_winning_view)
    await is_winning_view.wait()

    if not is_winning_view.is_winning:
        throw_view = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].first_player)
        await GameHolder.Game[ctx.guild].first_player.user.send("Choose a tile to get rid of:", view=throw_view)
        await throw_view.wait()

        await ctx.channel.send("<@" + str(GameHolder.Game[ctx.guild].first_player.user.id) + "> thrown the tile:")
        await ctx.channel.send(Emojis.get_emoji(str(throw_view.thrown_tile)))
        await ctx.channel.send("Here are all the thrown tiles:")
        await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))

        take_view: CustomViews.TakeView = CustomViews.TakeView(GameHolder.Game[ctx.guild].get_next_player(player),throw_view.thrown_tile)
        await ctx.send("Do you want to pickup this tile ?", view=take_view)
        await turn(GameHolder.Game[ctx.guild].get_next_player(player), ctx)
    else:
        await ctx.channel.send("<@" + str(GameHolder.Game[ctx.guild].first_player.user.id) + "> won !")
        await ctx.channel.send(Emojis.get_emojis([str(tile) for tile in GameHolder.Game[ctx.guild].first_player.shown_tiles.tiles]))
        await ctx.channel.send(Emojis.get_emojis([str(tile) for tile in GameHolder.Game[ctx.guild].first_player.tiles.tiles]))