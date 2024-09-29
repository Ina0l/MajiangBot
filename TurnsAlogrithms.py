import discord
from discord.ext.commands import Context
from discord.ui import View

from Objects import CustomViews, GameHolder
from Objects.CustomViews import ComboView
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

async def set_combos(player: Player) -> None:
    temporary_tiles = player.tiles
    if not temporary_tiles.get_combinations() is None:
        await player.user.send("choose how to organize your tiles")
        a=0
        while len(temporary_tiles.get_combinations()) > 0:
            a+=1
            view: View = ComboView(player, temporary_tiles.get_combinations())
            await player.user.send("set your "+find_name_for_int(a+1)+" combo", view=view)
            await view.wait()
            if player.last_set_combo is None:
                break
            else:
                player.combo_tiles.append(player.last_set_combo)
    else:
        await player.user.send("you don't have any possible combos with your current tiles")

async def first_turn(interaction: discord.Interaction = None, ctx: Context = None) -> None:
    if ctx is None:
        if not interaction is None:
            ctx = Context.from_interaction(interaction)
        else:
            raise Exception("both ctx and interaction arguments were None")

    await set_combos(GameHolder.Game[ctx.guild].first_player)
    if GameHolder.Game[ctx.guild].first_player.does_win():
        pass
    else:
        view: View = CustomViews.ThrowView(ctx=ctx, player=GameHolder.Game[ctx.guild].first_player)
        await GameHolder.Game[ctx.guild].first_player.user.send("Choose a tile to get rid of:", view=view)
        await view.wait()
