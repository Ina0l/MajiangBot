from random import choice
from typing import Any, Optional

import discord
from discord import SelectOption, ButtonStyle, Interaction
from discord._types import ClientT
from discord.ext.commands import Context

from Methods import Emojis
from Methods.Emojis import get_emoji
import Objects.GameHolder as GameHolder
from Objects.Player import Player
from Tiles import Tile


def throwing_tile(player: Player, ctx: Context, tile: Tile.Tile):
        player.throw_tile(tile)
        GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
        GameHolder.Game[ctx.guild].throwed_tiles.append(tile)
        GameHolder.Game[ctx.guild].throwed_tiles.last_thrown_tile = tile

async def set_combo():
    pass

class ThrowView(discord.ui.View):
    def __init__(self, *, ctx: Context, player: Player):
        self.ctx = ctx
        self.player = player
        super().__init__(timeout=300)
        self.add_item(ThrowSelection(ctx, player))
        self.thrown_tile: Optional[Tile.Tile] = None

    def on_timeout(self) -> None:
        self.thrown_tile = choice(self.player.tiles.tiles)
        throwing_tile(self.player, self.ctx, self.thrown_tile)
        self.stop()


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
                view: ThrowView = self.view
                view.thrown_tile = tile
                throwing_tile(self.player, self.ctx, tile)
                await self.player.user.send("tile "+Emojis.get_emoji(str(tile))+" thrown")
        self.view.stop()
        self.disabled = True

async def win_check(button):
    button.view.stop()

class ChooseToWinView(discord.ui.View):
    def __init__(self, user: discord.abc.Messageable):
        super().__init__()
        self.user = user
        self.add_item(IsWinningButton())
        self.add_item(IsntWinningButton())

    async def on_timeout(self) -> None:
        await self.user.send("You aren't winning")
        self.stop()

class IsWinningButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Yes", style=ButtonStyle.green)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await self.view.user.send("You chose to win")
        await win_check(self)

class IsntWinningButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="No", style=ButtonStyle.red)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        await self.view.user.send("You aren't winning")
        self.view.stop()

class TakeView(discord.ui.View):
    def __init__(self):
        super().__init__()