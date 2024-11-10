from random import choice
from typing import Any

import discord
from discord import SelectOption, ButtonStyle, Interaction
from discord._types import ClientT
from discord.ext.commands import Context

from Methods import Emojis
from Methods.Emojis import get_emoji
import Objects.GameHolder as GameHolder
from Objects.Player import Player
from Tiles import Tile


async def throwing_tile(player: Player, ctx: Context, tile: Tile.Tile):
    player.throw_tile(tile)
    GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
    GameHolder.Game[ctx.guild].throwed_tiles.append(tile)
    await ctx.channel.send("<@"+str(player.user.id)+">"+ " thrown the tile:")
    await ctx.channel.send(Emojis.get_emoji(str(tile)))
    await ctx.channel.send("Here are all the thrown tiles:")
    await ctx.channel.send(str(GameHolder.Game[ctx.guild].throwed_tiles))
    GameHolder.Game[ctx.guild].throwed_tiles.last_thrown_tile = tile

async def set_combo():
    pass

class ThrowSelection(discord.ui.Select):
    def __init__(self, ctx: Context, player: Player):
        self.player = player
        self.ctx = ctx
        options: list[SelectOption] = []
        for tile in self.player.tiles.get_unique_tiles().tiles:
            options.append(discord.SelectOption(label=tile.get_name(), emoji=get_emoji(str(tile)), description="throws tile "+tile.get_name()))
        super().__init__(placeholder="Select a tile to throw",options=options)

    async def callback(self, interaction: discord.Interaction) -> Any:
        for tile in self.player.tiles.tiles:
            if tile.get_name() == self.values[0]:
                await throwing_tile(self.player, self.ctx, tile)
                await self.player.user.send("tile "+Emojis.get_emoji(str(tile))+" thrown")
        self.disabled = True

class ThrowView(discord.ui.View):
    def __init__(self, *, ctx: Context, player: Player):
        self.ctx = ctx
        self.player = player
        super().__init__(timeout=300)
        self.add_item(ThrowSelection(ctx, player))

    def on_timeout(self) -> None:
        throwing_tile(self.player, self.ctx, choice(self.player.tiles.tiles))
        self.stop()


async def win_check(button):
    button.parent_wiew.clear_items()
    button.parent_wiew.stop()

class ChooseToWinView(discord.ui.View):
    def __init__(self, user: discord.abc.Messageable):
        super().__init__()
        self.user = user
        self.add_item(IsWinningButton(self))
        self.add_item(IsntWinningButton(self))

    async def on_timeout(self) -> None:
        await self.user.send("You aren't winning")
        self.clear_items()
        self.stop()

class IsWinningButton(discord.ui.Button):
    def __init__(self, view: ChooseToWinView):
        super().__init__(label="Yes", style=ButtonStyle.green)
        self.parent_wiew = view

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await self.parent_wiew.user.send("You chose to win")
        await win_check(self)

class IsntWinningButton(discord.ui.Button):
    def __init__(self, view: ChooseToWinView):
        super().__init__(label="No", style=ButtonStyle.red)
        self.parent_wiew = view

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await self.parent_wiew.user.send("You aren't winning")
        self.parent_wiew.clear_items()
        self.parent_wiew.stop()

