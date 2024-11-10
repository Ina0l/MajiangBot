from typing import Optional

import discord.user
from discord import Guild

from Tiles.DrawPile import DrawPile
from Objects.Player import Player
from Tiles.ThrownPile import ThrownPile
from Tiles.Tile import Tile
from random import choice


class GameHolder:
    def __init__(self):
        self.player_list: list[Player] = []
        self.draw_pile: DrawPile = DrawPile()
        self.throwed_tiles: ThrownPile = ThrownPile()
        self.first_player: Optional[Player] = None

    def get_player_by_discord_user(self, user: discord.user.User) -> discord.user.User:
        for player in self.player_list:
            if player.user == user:
                return user
        raise Exception(user.name+" not in this game")

    def throw_tile(self, tile: Tile):
        self.throwed_tiles.append(tile)

    def set_first_player(self):
        self.first_player: Player = choice(self.player_list)
        self.player_list.remove(self.first_player)
        self.player_list = [self.first_player]+self.player_list


Game: dict[Guild, GameHolder] = dict()
