from random import choice
from typing import Any

import discord
from discord import Interaction, SelectOption
from discord.ext.commands import Context

from Methods import Emojis
from Methods.Emojis import get_emoji
import Objects.GameHolder as GameHolder
from Objects.Player import Player
from Tiles import Tile
from Tiles import TileList


async def throwing_tile(player: Player, ctx: Context, tile: Tile.Tile):
    player.throw_tile(tile)
    GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
    GameHolder.Game[ctx.guild].throwed_tiles.append(tile)
    await ctx.send("<@"+str(player.user.id)+">"+ " thrown the tile:")
    await ctx.send(Emojis.get_emoji(str(tile)))
    await ctx.send("Here are all the thrown tiles:")
    await ctx.send(str(GameHolder.Game[ctx.guild].throwed_tiles))
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

class ComboSelection(discord.ui.Select):
    def __init__(self, player: Player, combo_list: list[TileList.TileList]):
        self.player = player
        self.combo_list = combo_list
        options = []
        for combo in combo_list:
            name = combo.tiles[0].get_name()+", "
            name += combo.tiles[1].get_name()+", "
            name += combo.tiles[2].get_name()
            options.append(discord.SelectOption(label=name, emoji=Emojis.get_emoji(str(combo.tiles[0])), description="use these tiles to form a combo"))
        options.append(discord.SelectOption(label="pass", emoji="✅", description="don't form other combos"))
        super().__init__(placeholder="Select a combo", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: Interaction) -> Any:
        if self.values[0] == "pass":
            self.player.last_set_combo = None
        else:
            tile_names = self.values[0].split(", ")
            tiles = TileList.TileList([])
            for tile_name in tile_names:
                tiles.append(self.player.tiles.get_tile_by_name(tile_name))
            self.player.last_set_combo = tiles

class ThrowView(discord.ui.View):
    def __init__(self, *, ctx: Context, player: Player):
        self.ctx = ctx
        self.player = player
        super().__init__(timeout=180)
        self.add_item(ThrowSelection(ctx, player))

    def on_timeout(self) -> None:
        throwing_tile(self.player, self.ctx, choice(self.player.tiles.tiles))
        self.stop()

class ComboView(discord.ui.View):
    def __init__(self, player: Player, combo_list: list[TileList.TileList]):
        self.player = player
        self.combo_list = combo_list
        super().__init__(timeout=180)
        self.add_item(ComboSelection(player, combo_list))

    def on_timeout(self) -> None:
        pass
