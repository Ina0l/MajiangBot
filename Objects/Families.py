from enum import StrEnum, Enum


class Families(StrEnum):
    TONG = "tong",
    TIAO = "tiao",
    WANG = "wang",
    FENG = "feng",
    JIAN = "jian"

def get_family(family: str) -> Families:
    if family == "tong":
        return Families.TONG
    if family == "tiao":
        return Families.TIAO
    if family == "wang":
        return Families.WANG
    if family == "feng":
        return Families.FENG
    if family == "jian":
        return Families.JIAN

class ComboTypes(Enum):
    CHI = 1
    PONG = 2
    KONG = 3

def get_combo_type(combo_type: ComboTypes) -> str:
    if combo_type == ComboTypes.CHI: return "Chi"
    if combo_type == ComboTypes.PONG: return "Pong"
    if combo_type == ComboTypes.KONG: return "Kong"