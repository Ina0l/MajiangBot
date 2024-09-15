from Objects.Families import *
from random import randint

from Tiles.Tile import Tile


class DrawPile:
    def __init__(self):
        self.tong = [None, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.tiao = [None, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.wang = [None, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.feng = [None, 4, 4, 4, 4]
        self.jian = [None, 4, 4, 4]

        self.tong_total = [None]
        self.tiao_total = [None]
        self.wang_total = [None]
        self.feng_total = [None]
        self.jian_total = [None]

        self.set_families_total()

    def reset_families_total(self) -> None:
        self.tong_total = [None]
        self.tiao_total = [None]
        self.wang_total = [None]
        self.feng_total = [None]
        self.jian_total = [None]

    def set_families_total(self) -> None:
        total = 0
        for family in Families:
            for tile_nb in getattr(self, family):
                if tile_nb is None:
                    continue
                total += tile_nb
                getattr(self, family+"_total").append(total)

    def get_count(self) -> int:
        count = 0
        for family in Families:
            for tile_nb in getattr(self, str(family)):
                if not tile_nb is None:
                    count += tile_nb
        return count

    def get_family_count(self, family: str) -> int:
        count = 0
        family_list = getattr(self, family)
        for tile_nb in family_list:
            if not tile_nb is None:
                count += tile_nb
        return count

    def get_tile_by_index(self, index: int) -> Tile:
        for family in Families:
            tile_nb = 0
            for tile_nb_total in getattr(self, family+"_total"):
                if not tile_nb_total is None:
                    if tile_nb_total < index:
                        pass
                    else:
                        return Tile(family, tile_nb)
                tile_nb += 1

    def draw(self) -> Tile:
        drawn_tile_nb = randint(1, self.get_count())
        return self.get_tile_by_index(drawn_tile_nb)

    def remove_tile(self, tile: Tile) -> None:
        getattr(self, tile.family)[tile.nb] -= 1
        self.reset_families_total()
        self.set_families_total()