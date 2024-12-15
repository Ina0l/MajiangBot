from random import choice
from typing import Any, Optional

import discord
from discord import SelectOption, ButtonStyle, Interaction
from discord.ext.commands import Context

from Methods import Emojis
from Methods.Emojis import get_emoji
import Objects.GameHolder as GameHolder
from Objects import Families
from Objects.Player import Player
from Tiles import Tile
from Tiles.TileList import TileList


def throwing_tile(player: Player, ctx: Context, tile: Tile.Tile):
        player.throw_tile(tile)
        GameHolder.Game[ctx.guild].draw_pile.remove_tile(tile)
        GameHolder.Game[ctx.guild].throwed_tiles.append(tile)
        GameHolder.Game[ctx.guild].throwed_tiles.last_thrown_tile = tile

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
                await interaction.response().send_message("tile " + Emojis.get_emoji(str(tile)) + " thrown")
        self.view.stop()
        self.disabled = True

async def win_check(button):
    button.view.stop()
    button.view.is_winning = True
    combos = button.view.player.shown_tiles
    button.view.player.win_tiles_list = button.view.player.tiles
    win_tiles_list: TileList = button.view.player.win_tiles_list
    while len(combos) < 5:
        pass
    if win_tiles_list[0].matches_tile(win_tiles_list[1]):
        button.view.win = True

class ChooseToWinView(discord.ui.View):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.is_winning = False
        self.win = False
        self.add_item(IsWinningButton()).add_item(IsntWinningButton())

    async def on_timeout(self) -> None:
        await self.player.user.send("You aren't winning")

class IsWinningButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Yes", style=ButtonStyle.green)

    async def callback(self, interaction: Interaction) -> Any:
        await interaction.response().send_message("You chose to win")
        await win_check(self)

class IsntWinningButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="No", style=ButtonStyle.red)

    async def callback(self, interaction: Interaction) -> Any:
        await interaction.response().send_message("You aren't winning")
        self.view.stop()

class TakeView(discord.ui.View):
    def __init__(self, is_chi_player: bool, player: Player, thrown_tile: Tile.Tile, ctx: Context):
        super().__init__()
        self.result_combo: Optional[list[Tile.Tile]] = None
        self.result_combo_type: Optional[Families.ComboTypes] = None
        self.add_item(TakeButton(thrown_tile, player, is_chi_player, ctx)).add_item(DontTakeButton())

class TakeButton(discord.ui.Button):
    def __init__(self, thrown_tile: Tile.Tile, player: Player, is_chi_player: bool, ctx: Context):
        self.thrown_tile = thrown_tile
        self.player = player
        self.is_chi_player = is_chi_player
        self.ctx = ctx
        super().__init__(label="Take", style=ButtonStyle.green)

    async def callback(self, interaction: Interaction) -> Any:
        combo_select_view = ComboSelectionView(self.thrown_tile, self.player, self.is_chi_player, self.ctx)
        await interaction.response().send_message("how are you gonna take this tile ?", view=combo_select_view)
        await combo_select_view.wait()
        self.view.result_combo = combo_select_view.result_combo
        self.view.result_combo_type = combo_select_view.result_combo_type
        self.view.stop()

class DontTakeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Don't take", style=ButtonStyle.red)

    async def callback(self, interaction: Interaction) -> Any:
        self.view.stop()
        await interaction.response().send_message("you chose not to take this tile")

class ComboSelectionView(discord.ui.View):
    def __init__(self, thrown_tile: Tile.Tile, player: Player, is_chi_player: bool, ctx: Context):
        super().__init__()
        self.result_combo: Optional[list[Tile.Tile]] = None
        self.result_combo_type: Optional[Families.ComboTypes] = None
        self.thrown_tile = thrown_tile
        self.add_item(ComboSelect(thrown_tile, player, is_chi_player, ctx))

class ComboSelect(discord.ui.Select):
    def __init__(self, thrown_tile: Tile.Tile, player: Player, is_chi_player: bool, ctx: Context):
        self.thrown_tile = thrown_tile
        self.player = player
        self.is_chi_player = is_chi_player
        self.ctx = ctx
        options: list[discord.SelectOption] = []
        if player.tiles.count(thrown_tile) == 3: options.append(discord.SelectOption(label=(thrown_tile.get_name()+" ")*3,
                                                                                     emoji=Emojis.get_emoji(str(thrown_tile)), description="Kong"))
        if player.tiles.count(thrown_tile) >=2: options.append(discord.SelectOption(label=(thrown_tile.get_name()+" ")*2,
                                                                                    emoji=Emojis.get_emoji(str(thrown_tile)), description="Pong"))
        if (not thrown_tile.is_special) and is_chi_player:
            has_one_less = (False if thrown_tile.nb==1 else player.tiles.has_tile(Tile.Tile(thrown_tile.family, thrown_tile.nb-1)))
            has_two_less = (False if not has_one_less else (False if thrown_tile.nb==2 else player.tiles.has_tile(Tile.Tile(thrown_tile.family, thrown_tile.nb-2))))
            has_one_more = (False if thrown_tile.nb==9 else player.tiles.has_tile(Tile.Tile(thrown_tile.family, thrown_tile.nb+1)))
            has_two_more = (False if not has_one_more else (False if thrown_tile.nb==8 else player.tiles.has_tile(Tile.Tile(thrown_tile.family, thrown_tile.nb+2))))

            if has_one_less and has_two_less: options.append(discord.SelectOption(label=Tile.Tile(thrown_tile.family, thrown_tile.nb-1).get_name()
                                                                                        +" "+Tile.Tile(thrown_tile.family, thrown_tile.nb-2).get_name(),
                                                                                        emoji=Emojis.get_emoji(str(thrown_tile)), description="Chi"))
            if has_one_less and has_one_more: options.append(discord.SelectOption(label=Tile.Tile(thrown_tile.family, thrown_tile.nb-1).get_name()
                                                                                        +" "+Tile.Tile(thrown_tile.family, thrown_tile.nb+1).get_name(),
                                                                                        emoji=Emojis.get_emoji(str(thrown_tile)), description="Chi"))
            if has_one_more and has_two_more: options.append(discord.SelectOption(label=Tile.Tile(thrown_tile.family, thrown_tile.nb+1).get_name()
                                                                                        +" "+Tile.Tile(thrown_tile.family, thrown_tile.nb+2).get_name(),
                                                                                        emoji=Emojis.get_emoji(str(thrown_tile)), description="Chi"))
        options.append(discord.SelectOption(label="Don't take", emoji="❌", description="Choose to finally not take the tile"))
        super().__init__(placeholder="choose a combination", options=options)

    async def callback(self, interaction: Interaction) -> Any:
        one_less_authorized = self.thrown_tile.nb > 1
        two_less_authorized = self.thrown_tile.nb > 2
        one_more_authorized = self.thrown_tile.nb < 9
        two_more_authorized = self.thrown_tile.nb < 8

        if self.values[0] == ((self.thrown_tile.get_name()+" ")*3)[:-1]:
            for a in range(3): self.player.tiles.remove(self.thrown_tile)
            self.player.shown_tiles.append(TileList([self.thrown_tile]*4))

            self.view.result_combo = [self.thrown_tile]*4
            self.view.result_combo_type = Families.ComboTypes.KONG
            tile = GameHolder.Game[self.ctx.guild].draw_pile.draw()
            GameHolder.Game[self.ctx.guild].draw_pile.remove_tile(tile)
            self.player.add_tile(tile)
            await interaction.response().send_message("Kong")

        elif self.values[0] == ((self.thrown_tile.get_name()+" ")*2)[:-1]:
            for a in range(2): self.player.tiles.remove(self.thrown_tile)
            self.player.shown_tiles.append(TileList([self.thrown_tile]*3))

            self.view.result_combo = [self.thrown_tile]*3
            self.view.result_combo_type = Families.ComboTypes.PONG
            await interaction.response().send_message("Pong")

        elif one_less_authorized and two_less_authorized and self.values[0] == (Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb-1).get_name()+" "+Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb-2).get_name()):
            self.player.tiles.remove(Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 1))
            self.player.tiles.remove(Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 2))
            self.player.shown_tiles.append(TileList([self.thrown_tile, Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 1), Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 2)]))

            self.view.result_combo = [self.thrown_tile, Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 1), Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 2)]
            self.view.result_combo_type = Families.ComboTypes.CHI
            await interaction.response().send_message("Chi")

        elif one_less_authorized and one_more_authorized and self.values[0] == (Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb-1).get_name()+" "+Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb+1).get_name()):
            self.player.tiles.remove(Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 1))
            self.player.tiles.remove(Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 1))
            self.player.shown_tiles.append(TileList([self.thrown_tile, Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 1), Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 1)]))

            self.view.result_combo = [self.thrown_tile, Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb - 1), Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 1)]
            self.view.result_combo_type = Families.ComboTypes.CHI
            await interaction.response().send_message("Chi")

        elif one_more_authorized and two_more_authorized and self.values[0] == (Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb+1).get_name()+" "+Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb+2).get_name()):
            self.player.tiles.remove(Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 1))
            self.player.tiles.remove(Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 2))
            self.player.shown_tiles.append(TileList([self.thrown_tile, Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 1), Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 2)]))

            self.view.result_combo = [self.thrown_tile, Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 1), Tile.Tile(self.thrown_tile.family, self.thrown_tile.nb + 2)]
            self.view.result_combo_type = Families.ComboTypes.CHI
            await interaction.response().send_message("Chi")

        elif self.values[0] == "Don't take":
            await interaction.response().send_message("you chose no to take the tile")
        self.view.stop()

class WinSelectionView(discord.ui.View):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.add_item(WinSelection(self.player))
        self.combo: Optional[TileList]

class WinSelection(discord.ui.Select):
    def __init__(self, player: Player):
        self.player = player
        options: list[SelectOption] = []
        combos = player.combo_tiles.get_combinations()
        for combo in combos:
            options.append(SelectOption(label=combo.get_tiles_name(), emoji=Emojis.get_emoji(str(combo[0])), value=str(combo),
                                        description=("Kong" if len(combo)==4 else ("Pong" if combo[0].matches_tile(combo[1]) else "Chi"))))
        options.append(SelectOption(label="Don't win", emoji="❌", description="Choose not to continue making combos"))
        super().__init__(placeholder="Choose a combo", options=options)

    async def callback(self, interaction: Interaction) -> Any:
        if self.values[0]=="Don't win":
            self.view.combo = None
        else:
            #TODO:
            pass