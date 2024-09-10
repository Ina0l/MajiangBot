from Families import Families


class Tile:
    def __init__(self, family: str, nb: int):
        self.family = family
        self.is_special = self.family in [Families.FENG, Families.JIAN]
        if not self.is_special:
            if 0 < nb < 10:
                self.nb = nb
            else:
                raise Exception("tile "+family+" "+str(nb)+" is out of range")
        elif family == Families.FENG:
            if 0 < nb <= 4:
                self.nb = nb
            else:
                raise Exception("tile "+family+" "+str(nb)+" is out of range")
        else:
            if 0 < nb <= 3:
                self.nb = nb
            else:
                raise Exception("tile "+family+" "+str(nb)+" is out of range")

    def __str__(self):
        string: str = ""
        string += str(self.nb)
        string += "_"
        string += self.family
        return string