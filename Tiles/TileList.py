from typing import Optional

from Objects.Families import Families, get_family
from Tiles.SortingObject import SortingObject
from Tiles.Tile import Tile


def get_every_tiles(tile_lists: list["TileList"]) -> "TileList":
    tiles = TileList([])
    for tile_list in tile_lists:
        for tile in tile_list.tiles:
            tiles.append(tile)
    return tiles


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

    def get_tile_by_name(self, name: str) -> Tile:
        if not name[0].isnumeric():
            raise TypeError("name must start with a digit")
        else:
            for tile in self.tiles:
                if "_" in name:
                    if str(tile) == name:
                        return tile
                else:
                    if tile.get_name() == name:
                        return tile
        raise TypeError("the name", name, "doesn't match the format for tile name or id")

    def append(self, tile: Tile) -> None:
        self.tiles.append(tile)

    def remove(self, removing_tile: Tile) -> None:
        for tile in self.tiles:
            if removing_tile.matches_tile(tile): self.tiles.remove(tile)

    def count(self, tile_to_count: Tile) -> int:
        tile_nb: int = 0
        for tile in self.tiles:
            if tile.matches_tile(tile_to_count): tile_nb += 1
        return tile_nb

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

    def has_tile(self, tile_to_check: Tile) -> bool:
        for tile in self.tiles:
            if tile.matches_tile(tile_to_check):
                return True
        return False

    def matches_list(self, tile_list: "TileList") -> bool:
        matches = True
        for tile in self.tiles:
            for tile_to_check in tile_list.tiles:
                if tile.matches_tile(tile_to_check):
                    matches = False
        return matches

    def is_tile_list_in_list(self, tile_list_list: list["TileList"]) -> bool:
        is_in = False
        for tile_list in tile_list_list:
            if self.matches_list(tile_list):
                is_in = True
        return is_in

    def get_combinations(self) -> Optional[list["TileList"]]:
        tile_combinations: list[TileList] = []
        for tile in self.tiles:
            if self.count(tile) >= 3:
                if not TileList([tile, tile, tile]).is_tile_list_in_list(tile_combinations):
                    tile_combinations.append(TileList([tile, tile, tile]))
            if self.count(tile) == 4:
                if not TileList([tile, tile, tile]).is_tile_list_in_list(tile_combinations):
                    tile_combinations.append(TileList([tile, tile, tile, tile]))

            if not tile.is_special:
                one_more_tile: Optional[Tile] = None
                two_more_tile: Optional[Tile] = None
                one_less_tile: Optional[Tile] = None
                two_less_tile: Optional[Tile] = None

                if not tile.nb > 8:
                    one_more_tile = Tile(tile.family, tile.nb+1)
                    if not tile.nb > 7:
                        two_more_tile = Tile(tile.family, tile.nb+2)
                if not tile.nb < 3:
                    one_less_tile = Tile(tile.family, tile.nb-1)
                    if not tile.nb < 2:
                        two_less_tile = Tile(tile.family, tile.nb-2)


                if (not one_more_tile is None) and one_more_tile in self.tiles:
                    if (not two_more_tile is None) and self.has_tile(two_more_tile):
                        if not TileList([tile, one_more_tile, two_more_tile]).is_tile_list_in_list(tile_combinations):
                            tile_combinations.append(TileList([tile, one_more_tile, two_more_tile]))

                    if (not one_less_tile is None) and self.has_tile(one_less_tile):
                        if not TileList([one_less_tile, tile, one_more_tile]).is_tile_list_in_list(tile_combinations):
                            tile_combinations.append(TileList([one_less_tile, tile, one_more_tile]))

                if (not one_less_tile is None) and self.has_tile(one_less_tile):
                    if (not two_less_tile is None) and two_less_tile in self.tiles:
                        if not TileList([two_less_tile, one_less_tile, tile]).is_tile_list_in_list(tile_combinations):
                            tile_combinations.append(TileList([two_less_tile, one_less_tile, tile]))

                    if (not one_more_tile is None) and self.has_tile(one_more_tile):
                        if not TileList([one_less_tile, tile, one_more_tile]).is_tile_list_in_list(tile_combinations):
                            tile_combinations.append(TileList([one_less_tile, tile, one_more_tile]))
        return None if len(tile_combinations) == 0 else tile_combinations

    def get_unique_tiles(self) -> "TileList":
        unique_tiles = TileList([])
        for tile in self.tiles:
            is_tile_unique: bool = True
            for unique_tile in unique_tiles.tiles:
                if tile.matches_tile(unique_tile):
                    is_tile_unique = False
            if is_tile_unique:
                unique_tiles.append(tile)
        return unique_tiles

    def get_str_list(self) -> list[str]: return [str(tile) for tile in self.tiles]