import Bot
from Methods.Emojis import get_emoji
from Tiles.Tile import Tile
from Tiles.TileList import TileList


class ThrownPile:
    def __init__(self):
        self.tiles: TileList = TileList([])

    def append(self, tile: Tile):
        self.tiles.append(tile)

    def remove(self, tile: Tile):
        self.tiles.remove(tile)

    def __str__(self):
        self.tiles.sort()
        tile_list = []
        temporary_tile_list = ""
        for tile in self.tiles.tiles:
            if len(temporary_tile_list) < 6:
                temporary_tile_list += get_emoji(Bot.bot, str(tile))
            else:
                tile_list.append(temporary_tile_list)
                temporary_tile_list = get_emoji(Bot.bot, str(tile))
        tile_list.append(temporary_tile_list)

        tiles_string = ""
        for string in temporary_tile_list:
            tiles_string += string
            tiles_string += "\n"
        return tiles_string[:-1]
