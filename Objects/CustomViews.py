from random import choice
from typing import Any

import discord
from discord.ext.commands import Context

import Bot
from Methods import Emojis
from Methods.Emojis import get_emoji
import GameHolder
from Objects.Player import Player
from Tiles.Tile import Tile


async def throwing_tile(player: Player, ctx: Context, tile: Tile):
    player.throw_tile(tile)
    GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
    await ctx.send("<@"+str(player.user.id)+">"+ "thrown tile:")
    await ctx.send(Emojis.get_emoji(Bot.bot, str(tile)))
    await ctx.send("Here are all the thrown tiles:")
    await ctx.send(GameHolder.Game[ctx.guild])
    GameHolder.Game[ctx.guild].last_thrown_tile = tile

class ThrowSelection(discord.ui.Select):
    def __init__(self, ctx: Context, player: Player):
        self.player = player
        self.ctx = ctx
        options = []
        for tile in self.player.tiles.tiles:
            options.append(discord.SelectOption(label=tile.get_name(), emoji=get_emoji(Bot.bot, str(tile)), description="throws tile "+tile.get_name()))
        super().__init__(placeholder="Select a tile to throw",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction) -> Any:
        for tile in self.player.tiles.tiles:
            if tile.get_name() == self.values[0]:
                await throwing_tile(self.player, self.ctx, tile)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, ctx: Context, player: Player):
        self.ctx = ctx
        self.player = player
        super().__init__(timeout=timeout)
        self.add_item(ThrowSelection(ctx, player))

    def on_timeout(self) -> None:
        throwing_tile(self.player, self.ctx, choice(self.player.tiles.tiles))
