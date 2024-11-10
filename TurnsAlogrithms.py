import discord
from discord.ui import View
import discord.ext.commands.context as context

from Methods import Emojis
from Objects import CustomViews, GameHolder
from Objects.Player import Player


def find_name_for_int(integer: int) -> str:
    if str(integer)[-1] == "1":
        return str(integer)+"st"
    elif str(integer)[-1] == "2":
        return str(integer)+"nd"
    elif str(integer)[-1] == "3":
        return str(integer)+"rd"
    else:
        return str(integer)+"th"

async def first_turn(interaction: discord.Interaction = None, ctx: context.Context = None) -> None:
    if ctx is None:
        if not interaction is None:
            ctx = await context.Context.from_interaction(interaction)
        else:
            raise Exception("both ctx and interaction arguments were None")

    is_winning_view: View = CustomViews.ChooseToWinView(GameHolder.Game[ctx.guild].first_player.user)
    await GameHolder.Game[ctx.guild].first_player.user.send("Are you currently winning ?", view=is_winning_view)
    await is_winning_view.wait()
    throw_view = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].first_player)
    await GameHolder.Game[ctx.guild].first_player.user.send("Choose a tile to get rid of:", view=throw_view)
    await throw_view.wait()
    await ctx.channel.send("<@"+str(GameHolder.Game[ctx.guild].first_player.user.id)+">"+ " thrown the tile:")
    await ctx.channel.send(Emojis.get_emoji(str(throw_view.thrown_tile)))
    await ctx.channel.send("Here are all the thrown tiles:")
    await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))
    take_view = CustomViews.TakeView()
    await turn(GameHolder.Game[ctx.guild].player_list[1], ctx)

async def turn(player: Player, ctx: context.Context) -> None:
    pass