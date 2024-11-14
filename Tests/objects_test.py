from Tiles import TileList, DrawPile, Tile
from Objects import Families

# tiles = TileList.TileList([])
# drawing_pile = DrawPile.DrawPile()
# for a in range(32):
#     tile = drawing_pile.draw()
#     drawing_pile.remove_tile(tile)
#     tiles.append(tile)

def funct(str_: str) -> Tile.Tile:
    return Tile.Tile(Families.get_family(str_.split("_")[1]), int(str_.split("_")[0]))

liste = ['5_tiao', '5_tong', '6_tong', '2_tong', '8_wang', '1_jian', '5_wang', '9_wang', '7_wang', '4_wang', '4_tiao', '7_tong', '7_tiao', '8_tiao', '9_tong', '9_tong', "1_tiao", '1_tiao', '4_tiao', '6_tiao', '3_tong', '2_jian', '1_jian', '2_tiao', '5_tong', '5_wang', '5_wang', '5_tiao', '8_wang', '1_tong', '3_tong', '9_tiao']

tiles = TileList.TileList([funct(str_) for str_ in liste])

print(tiles.get_str_list())
tiles.sort()
print(tiles.get_str_list())