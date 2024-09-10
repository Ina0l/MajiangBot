from Families import Families
from DrawPile import DrawPile
from Tile import Tile


drawpile = DrawPile()

drawpile.remove_tile(Tile(Families.FENG, 4))
drawpile.remove_tile(Tile(Families.FENG, 3))
drawpile.remove_tile(Tile(Families.JIAN, 3))

for a in range(1, drawpile.get_count()+1):
    print(drawpile.get_tile_by_index(a))
