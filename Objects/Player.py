from typing import Optional

from discord import User

from Tiles.Tile import Tile
from Tiles.TileList import TileList


class Player:
    def __init__(self, user: User):
        self.user: User = user
        self.score = 0
        self.tiles: TileList = TileList([])
        self.shown_tiles: TileList = TileList([])
        self.combo_tiles: list[TileList] = []
        self.not_combo_tiles: TileList = TileList([])
        self.last_set_combo: Optional[TileList] = None
        self.combos_nb: int

    def __str__(self):
        return self.user.name

    def add_tile(self, tile: Tile) -> None:
        self.tiles.append(tile)

    def throw_tile(self, tile: Tile) -> None:
        if tile in self.tiles:
            self.tiles.remove(tile)
        else:
            raise Exception("player: "+self.user.name+" does not have the tile: "+str(tile))

    def show_tile(self, tile: Tile) -> None:
        self.throw_tile(tile)
        self.shown_tiles.append(tile)

    def kong_check(self) -> None:
        for tile in self.tiles:
            if self.tiles.count(tile) == 4:
                for a in range(4): self.tiles.remove(tile)
                for a in range(4): self.shown_tiles.append(Tile(tile.family, tile.nb))
                self.kong_check()
                break