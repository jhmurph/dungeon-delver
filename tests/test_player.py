"""Tests for the Player class."""

import pytest
from dungeon.player import Player
from dungeon.config import PLAYER_START_HP, PLAYER_START_ATTACK, MAX_INVENTORY_SIZE
from dungeon.items import HealingPotion


class TestPlayerInit:
    def test_default_stats(self):
        p = Player("Hero")
        assert p.name == "Hero"
        assert p.hp == PLAYER_START_HP
        assert p.max_hp == PLAYER_START_HP
        assert p.level == 1
        assert p.experience == 0
        assert p.gold == 0
        assert p.kills == 0

    def test_empty_inventory_on_start(self):
        p = Player("Hero")
        assert p.inventory == []

    def test_is_alive_at_start(self):
        p = Player("Hero")
        assert p.is_alive()


class TestPlayerCombat:
    def test_take_damage_reduces_hp(self):
        p = Player("Hero")
        p.take_damage(10)
        assert p.hp == PLAYER_START_HP - 10

    def test_take_damage_minimum_is_1(self):
        p = Player("Hero")
        dealt = p.take_damage(0)
        assert dealt == 1
        assert p.hp == PLAYER_START_HP - 1

    def test_hp_cannot_go_below_zero(self):
        p = Player("Hero")
        p.take_damage(9999)
        assert p.hp == 0

    def test_dead_when_hp_zero(self):
        p = Player("Hero")
        p.hp = 0
        assert not p.is_alive()

    def test_heal_restores_hp(self):
        p = Player("Hero")
        p.hp = 50
        healed = p.heal(20)
        assert healed == 20
        assert p.hp == 70

    def test_heal_capped_at_max_hp(self):
        p = Player("Hero")
        p.hp = p.max_hp - 5
        healed = p.heal(100)
        assert p.hp == p.max_hp
        assert healed == 5

    def test_heal_returns_zero_when_already_full(self):
        p = Player("Hero")
        healed = p.heal(50)
        assert healed == 0
        assert p.hp == p.max_hp


class TestPlayerLeveling:
    def test_add_experience_accumulates(self):
        p = Player("Hero")
        p.add_experience(50)
        assert p.experience == 50

    def test_level_up_on_threshold(self):
        p = Player("Hero")
        p.add_experience(p.xp_threshold)
        assert p.level == 2

    def test_level_up_increases_attack(self):
        p = Player("Hero")
        old_attack = p.attack
        p.add_experience(p.xp_threshold)
        assert p.attack > old_attack

    def test_level_up_increases_defense(self):
        p = Player("Hero")
        old_def = p.defense
        p.add_experience(p.xp_threshold)
        assert p.defense > old_def

    def test_level_up_increases_max_hp(self):
        p = Player("Hero")
        old_max = p.max_hp
        p.add_experience(p.xp_threshold)
        assert p.max_hp > old_max

    def test_level_up_resets_experience(self):
        p = Player("Hero")
        p.add_experience(p.xp_threshold + 50)
        assert p.experience == 0


class TestPlayerInventory:
    def test_add_item_succeeds(self):
        p = Player("Hero")
        potion = HealingPotion()
        result = p.add_item(potion)
        assert result is True
        assert potion in p.inventory

    def test_remove_item_succeeds(self):
        p = Player("Hero")
        potion = HealingPotion()
        p.add_item(potion)
        result = p.remove_item(potion)
        assert result is True
        assert potion not in p.inventory

    def test_remove_missing_item_returns_false(self):
        p = Player("Hero")
        result = p.remove_item(HealingPotion())
        assert result is False

    def test_inventory_capacity_is_limited(self):
        p = Player("Hero")
        added = sum(1 for _ in range(MAX_INVENTORY_SIZE + 2) if p.add_item(HealingPotion()))
        assert added == MAX_INVENTORY_SIZE - 1

    def test_get_stat_returns_value(self):
        p = Player("Hero")
        assert p.get_stat("attack") == PLAYER_START_ATTACK

    def test_get_stat_unknown_returns_none(self):
        p = Player("Hero")
        assert p.get_stat("nonexistent_stat") is None
