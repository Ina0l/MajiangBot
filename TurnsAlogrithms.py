import discord
from discord.ext.commands import Context

from Objects import CustomViews, GameHolder


async def first_turn(interaction: discord.Interaction = None, ctx: Context = None) -> None:
    if ctx is None:
        if not interaction is None:
            ctx = Context.from_interaction(interaction)
        else:
            raise Exception("both ctx and interaction arguments were None")

    if GameHolder.Game[ctx.guild].first_player.does_win():
        pass
    else:
        await GameHolder.Game[ctx.guild].first_player.user.send("Choose a tile to get rid of:", view=(
            CustomViews.SelectView(ctx=ctx, player=GameHolder.Game[ctx.guild].first_player)))
        await ctx.send("hello")
