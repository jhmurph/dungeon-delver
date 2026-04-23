"""Tests for the combat system."""

import pytest
from dungeon.player import Player
from dungeon.monster import MonsterFactory
from dungeon.combat import Combat, CombatResult


@pytest.fixture
def player():
    return Player("TestHero")


@pytest.fixture
def goblin():
    return MonsterFactory.create("goblin", floor=1)


@pytest.fixture
def combat(player, goblin):
    return Combat(player, goblin)


class TestCombatState:
    def test_initial_status_is_ongoing(self, combat):
        assert combat.get_status() == CombatResult.ONGOING

    def test_status_player_win_when_monster_dead(self, combat):
        combat.monster.hp = 0
        assert combat.get_status() == CombatResult.PLAYER_WIN

    def test_status_player_dead_when_player_dead(self, combat):
        combat.player.hp = 0
        assert combat.get_status() == CombatResult.PLAYER_DEAD

    def test_turn_counter_increments(self, combat):
        combat.player_attack()
        assert combat.turn == 1
        combat.player_attack()
        assert combat.turn == 2


class TestPlayerAttack:
    def test_player_attack_reduces_monster_hp(self, combat):
        before = combat.monster.hp
        combat.player_attack()
        assert combat.monster.hp < before

    def test_player_attack_logs_message(self, combat):
        combat.player_attack()
        assert len(combat.log) == 1
        assert "hit" in combat.log[0].lower()


class TestMonsterAttack:
    def test_monster_attack_reduces_player_hp(self, combat):
        before = combat.player.hp
        combat.monster_attack()
        assert combat.player.hp < before

    def test_monster_attack_logs_message(self, combat):
        combat.monster_attack()
        assert len(combat.log) == 1
        assert "attacks" in combat.log[0].lower()


class TestFullTurn:
    def test_do_turn_returns_two_messages(self, combat):
        p_msg, m_msg = combat.do_turn()
        assert isinstance(p_msg, str) and len(p_msg) > 0
        assert isinstance(m_msg, str) and len(m_msg) > 0

    def test_do_turn_no_monster_retaliation_if_dead(self, combat):
        combat.monster.hp = 1  # will die on player attack
        p_msg, m_msg = combat.do_turn()
        assert m_msg == ""


class TestVictoryRewards:
    def test_xp_awarded_on_victory(self, combat):
        before = combat.player.experience
        combat.monster.hp = 0
        combat.award_victory()
        assert combat.player.experience > before

    def test_gold_awarded_on_victory(self, combat):
        before = combat.player.gold
        combat.monster.hp = 0
        combat.award_victory()
        assert combat.player.gold > before

    def test_kill_count_incremented(self, combat):
        combat.monster.hp = 0
        combat.award_victory()
        assert combat.player.kills == 1


class TestFlee:
    def test_flee_always_returns_false(self, combat):
        result = combat.flee()
        assert result is False
