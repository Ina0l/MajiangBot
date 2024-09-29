import discord

import Bot


def get_emoji(name: str) -> str:
    return str(discord.utils.get(Bot.bot.emojis, name=name))

def get_full_emoji_list() -> list[str]:
    emojis_list = []
    for emoji_name in emojis_list_str:
        emojis_list.append(get_emoji(emoji_name))
    return emojis_list

emojis_list_str = ["1_tong", "2_tong", "3_tong", "4_tong", "5_tong", "6_tong", "7_tong", "8_tong", "9_tong",
                   "1_tiao", "2_tiao", "3_tiao", "4_tiao", "5_tiao", "6_tiao", "7_tiao", "8_tiao", "9_tiao",
                   "1_wang", "2_wang", "3_wang", "4_wang", "5_wang", "6_wang", "7_wang", "8_wang", "9_wang",
                   "1_feng", "2_feng", "3_feng", "4_feng",
                   "1_jian", "2_jian", "3_jian"]