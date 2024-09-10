from Families import Families
from DrawPile import DrawPile
from Tile import Tile


draw_pile = DrawPile()

draw_pile.remove_tile(Tile(Families.FENG, 4))
draw_pile.remove_tile(Tile(Families.FENG, 3))
draw_pile.remove_tile(Tile(Families.JIAN, 3))

for a in range(1, draw_pile.get_count()+1):
    print(draw_pile.get_tile_by_index(a))
