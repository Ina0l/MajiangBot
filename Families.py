from enum import StrEnum


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