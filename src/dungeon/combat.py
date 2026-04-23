"""Combat system for Dungeon Delver."""

import random
from dungeon.config import BASE_CRIT_CHANCE, CRIT_MULTIPLIER
from dungeon.player import Player
from dungeon.monster import Monster


class CombatResult:
    ONGOING = "ongoing"
    PLAYER_WIN = "player_win"
    PLAYER_FLED = "player_fled"
    PLAYER_DEAD = "player_dead"


class Combat:
    """Manages a combat encounter between the player and a monster.

    Turn order: player attacks first, then monster retaliates (if still alive).
    Critical hits are only possible on player attacks.
    """

    def __init__(self, player: Player, monster: Monster):
        self.player = player
        self.monster = monster
        self.turn = 0
        self.log: list[str] = []

    def player_attack(self) -> str:
        """Player attacks the monster. Returns a description of what happened."""
        self.turn += 1

        raw_damage = random.randint(
            max(1, self.player.attack - 3),
            self.player.attack + 3,
        )

        is_crit = random.random() < BASE_CRIT_CHANCE
        if is_crit:
            raw_damage = int(raw_damage * CRIT_MULTIPLIER)

        dealt = self.monster.take_damage(raw_damage)
        msg = f"You hit the {self.monster.name} for {dealt} damage"
        if is_crit:
            msg += " (CRITICAL HIT!)"
        msg += f". ({self.monster.hp}/{self.monster.max_hp} HP remaining)"

        self.log.append(msg)
        return msg

    def monster_attack(self) -> str:
        """Monster attacks the player. Returns a description of what happened."""
        raw = random.randint(max(1, self.monster.attack - 2), self.monster.attack + 2)
        reduced = max(1, raw - self.player.defense)
        actual = self.player.take_damage(reduced)

        msg = f"The {self.monster.name} attacks you for {actual} damage."
        msg += f" ({self.player.hp}/{self.player.max_hp} HP remaining)"
        self.log.append(msg)
        return msg

    def do_turn(self) -> tuple[str, str]:
        """Execute one full combat turn (player then monster). Returns (player_msg, monster_msg)."""
        p_msg = self.player_attack()
        m_msg = ""
        if self.monster.is_alive():
            m_msg = self.monster_attack()
        return p_msg, m_msg

    def get_status(self) -> str:
        if not self.player.is_alive():
            return CombatResult.PLAYER_DEAD
        if not self.monster.is_alive():
            return CombatResult.PLAYER_WIN
        return CombatResult.ONGOING

    def award_victory(self):
        """Grant XP and gold to the player after defeating the monster."""
        self.player.add_experience(self.monster.xp_reward)
        self.player.gold += self.monster.gold_reward
        self.player.kills += 1
        print(f"\nVictory! You earned {self.monster.xp_reward} XP and {self.monster.gold_reward} gold.")
        # TODO: trigger item drops from monster.loot_table

    def flee(self) -> bool:
        """Attempt to flee from combat. Returns True if successful."""
        # TODO: implement flee using FLEE_SUCCESS_CHANCE
        print("You attempt to flee but can't find an opening!")
        return False
