from discord import User

from Tiles.Tile import Tile
from Tiles.TileList import TileList


class Player:
    def __init__(self, user: User):
        self.user: User = user
        self.score = 0
        self.tiles: TileList = TileList([])
        self.shown_tiles: TileList = TileList([])

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

    def does_win(self) -> bool:
        pass