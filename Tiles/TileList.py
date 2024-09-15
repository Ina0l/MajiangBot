from Objects.Families import Families, get_family
from SortingObject import SortingObject
from Tile import Tile


class TileList:
    def __init__(self, tiles: list[Tile]):
        self.tiles: list[Tile] = tiles

    def __getitem__(self, item: str|int):
        if type(item) == "<class 'str'>":
            if item in Families:
                return self.get_family(get_family(str(item)))
            else:
                return IndexError(item+" doesn't exist in this TileList")
        else:
            return self.tiles[item]

    def append(self, tile: Tile) -> None:
        self.tiles.append(tile)

    def remove(self, tile: Tile) -> None:
        self.tiles.remove(tile)

    def get_family(self, family: Families) -> list[Tile]:
        family_tile_list: list[Tile] = []
        for tile in self.tiles:
            if tile.family == family:
                family_tile_list.append(tile)
        return family_tile_list

    def sort(self) -> None:
        tong_sorting = SortingObject(self.get_family(Families.TONG))
        tiao_sorting = SortingObject(self.get_family(Families.TIAO))
        wang_sorting = SortingObject(self.get_family(Families.WANG))
        feng_sorting = SortingObject(self.get_family(Families.FENG))
        jian_sorting = SortingObject(self.get_family(Families.JIAN))

        tong_list = tong_sorting.concatenate()
        tiao_list = tiao_sorting.concatenate()
        wang_list = wang_sorting.concatenate()
        feng_list = feng_sorting.concatenate()
        jian_list = jian_sorting.concatenate()

        tile_list = tong_list
        for tile in tiao_list:
           tile_list.append(tile)
        for tile in wang_list:
            tile_list.append(tile)
        for tile in feng_list:
           tile_list.append(tile)
        for tile in jian_list:
            tile_list.append(tile)

        self.tiles = tile_list

    def count_combinations(self) -> int:
        pass