from Tiles.Tile import Tile


class SortingObject:
    def __init__(self, tiles: list[Tile]):
        self.list_1 = []
        self.list_2 = []
        self.list_3 = []
        self.list_4 = []
        self.list_5 = []
        self.list_6 = []
        self.list_7 = []
        self.list_8 = []
        self.list_9 = []

        for tile in tiles:
            if tile.nb == 1:
                self.list_1.append(tile)
            if tile.nb == 2:
                self.list_2.append(tile)
            if tile.nb == 3:
                self.list_3.append(tile)
            if tile.nb == 4:
                self.list_4.append(tile)
            if tile.nb == 5:
                self.list_5.append(tile)
            if tile.nb == 6:
                self.list_5.append(tile)
            if tile.nb == 7:
                self.list_7.append(tile)
            if tile.nb == 8:
                self.list_8.append(tile)
            if tile.nb == 9:
                self.list_9.append(tile)

    def concatenate(self) -> list[Tile]:
        tile_list = self.list_1

        for tile in self.list_2:
            tile_list.append(tile)
        for tile in self.list_3:
            tile_list.append(tile)
        for tile in self.list_4:
            tile_list.append(tile)
        for tile in self.list_5:
            tile_list.append(tile)
        for tile in self.list_6:
            tile_list.append(tile)
        for tile in self.list_7:
            tile_list.append(tile)
        for tile in self.list_8:
            tile_list.append(tile)
        for tile in self.list_9:
            tile_list.append(tile)

        return tile_list