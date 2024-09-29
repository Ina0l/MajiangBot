from Objects.Families import Families

feng_names: dict[int: str] = {1: "dong", 2: "nan", 3: "xi", 4: "bei"}
jian_names: dict[int: str] = {1: "zhong", 2: "fa", 3: "bai"}


class Tile:
    def __init__(self, family: str, nb: int):
        self.family = family
        self.is_special = self.family in [Families.FENG, Families.JIAN]
        if not self.is_special:
            if 0 < nb < 10:
                self.nb = nb
            else:
                raise IndexError("tile "+family+" "+str(nb)+" is out of range")
        elif family == Families.FENG:
            if 0 < nb <= 4:
                self.nb = nb
            else:
                raise IndexError("tile "+family+" "+str(nb)+" is out of range")
        else:
            if 0 < nb <= 3:
                self.nb = nb
            else:
                raise IndexError("tile "+family+" "+str(nb)+" is out of range")

    def __str__(self):
        string: str = ""
        string += str(self.nb)
        string += "_"
        string += self.family
        return string

    def get_name(self) -> str:
        if not self.is_special:
            return str(self.nb)+" "+self.family
        elif self.family == "feng":
            return feng_names[self.nb]
        else:
            return jian_names[self.nb]

    def matches_tile(self, tile: "Tile") -> bool:
        return str(self) == str(tile)