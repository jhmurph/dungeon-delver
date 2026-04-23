"""Tests for game items."""

import pytest
from dungeon.player import Player
from dungeon.items import (
    HealingPotion,
    Weapon,
    Armor,
    PoisonPotion,
    create_item,
    COMMON_ITEMS,
    UNCOMMON_ITEMS,
    RARE_ITEMS,
)
from dungeon.config import POTION_HEAL_AMOUNT, ELIXIR_HEAL_AMOUNT


@pytest.fixture
def injured_player():
    p = Player("Tester")
    p.hp = 30
    return p


class TestHealingPotion:
    def test_minor_potion_heals(self, injured_player):
        potion = HealingPotion("minor")
        potion.use(injured_player)
        assert injured_player.hp == 30 + POTION_HEAL_AMOUNT

    def test_major_potion_heals_more_than_minor(self, injured_player):
        assert HealingPotion("major").heal_amount > HealingPotion("minor").heal_amount

    def test_healing_capped_at_max_hp(self):
        p = Player("Tester")
        p.hp = p.max_hp - 5
        HealingPotion("major").use(p)
        assert p.hp == p.max_hp

    def test_use_returns_descriptive_message(self, injured_player):
        msg = HealingPotion("minor").use(injured_player)
        assert "restore" in msg.lower() or "hp" in msg.lower()

    def test_inventory_unchanged_after_use(self):
        p = Player("Tester")
        potion = HealingPotion()
        p.add_item(potion)
        potion.use(p)
        assert potion in p.inventory

    def test_unknown_strength_defaults_to_minor_amount(self):
        potion = HealingPotion("legendary")
        assert potion.heal_amount == POTION_HEAL_AMOUNT


class TestWeapon:
    def test_equip_increases_attack(self):
        p = Player("Tester")
        old_atk = p.attack
        Weapon("Dagger", attack_bonus=3).use(p)
        assert p.attack == old_atk + 3

    def test_equipped_flag_set_after_use(self):
        p = Player("Tester")
        sword = Weapon("Sword", attack_bonus=5)
        assert not sword.equipped
        sword.use(p)
        assert sword.equipped

    def test_reuse_weapon(self):
        p = Player("Tester")
        old_atk = p.attack
        sword = Weapon("Sword", attack_bonus=5)
        sword.use(p)
        sword.use(p)
        assert p.attack == old_atk + 10


class TestArmor:
    def test_equip_increases_defense(self):
        p = Player("Tester")
        old_def = p.defense
        Armor("Shield", defense_bonus=4).use(p)
        assert p.defense == old_def + 4


class TestPoisonPotion:
    def test_use_returns_message(self):
        p = Player("Tester")
        msg = PoisonPotion().use(p)
        assert isinstance(msg, str) and len(msg) > 0

    def test_use_does_not_modify_player(self):
        p = Player("Tester")
        before_hp = p.hp
        PoisonPotion().use(p)
        assert p.hp == before_hp


class TestItemFactory:
    def test_create_known_item(self):
        item = create_item("minor_potion")
        assert item is not None

    def test_create_unknown_item_returns_none(self):
        assert create_item("vorpal_bunny_slipper") is None

    def test_all_common_items_creatable(self):
        for key in COMMON_ITEMS:
            assert create_item(key) is not None, f"Failed to create: {key}"

    def test_all_uncommon_items_creatable(self):
        for key in UNCOMMON_ITEMS:
            assert create_item(key) is not None, f"Failed to create: {key}"

    def test_all_rare_items_creatable(self):
        for key in RARE_ITEMS:
            assert create_item(key) is not None, f"Failed to create: {key}"
