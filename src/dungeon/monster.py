"""Monster definitions and factory."""

import random
from dataclasses import dataclass, field
from typing import List


@dataclass
class LootEntry:
    item_name: str
    chance: float
    gold_min: int = 0
    gold_max: int = 0


@dataclass
class Monster:
    """A dungeon monster.

    Note: loot_table is defined but loot dropping is not yet wired up in the combat module.
    """

    name: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    xp_reward: int
    gold_reward: int
    description: str = ""
    loot_table: List[LootEntry] = field(default_factory=list)

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount)
        self.hp = max(0, self.hp - actual)
        return actual

    def attackPlayer(self, player) -> int:  # inconsistency: camelCase
        """Perform an attack against the player. Returns damage dealt."""
        damage = random.randint(max(1, self.attack - 2), self.attack + 2)
        return player.take_damage(damage)

    def getStatus(self) -> str:  # inconsistency: camelCase
        hp_pct = self.hp / self.max_hp
        if hp_pct > 0.75:
            return "healthy"
        elif hp_pct > 0.4:
            return "wounded"
        elif hp_pct > 0.1:
            return "badly wounded"
        else:
            return "near death"


class MonsterFactory:
    """Creates monsters appropriate for the given dungeon floor."""

    MONSTER_TEMPLATES = {
        "goblin": {
            "name": "Goblin",
            "hp": 20,
            "attack": 6,
            "defense": 2,
            "xp_reward": 15,
            "gold_reward": 5,
            "description": "A small, green-skinned menace with beady red eyes.",
        },
        "skeleton": {
            "name": "Skeleton",
            "hp": 30,
            "attack": 8,
            "defense": 4,
            "xp_reward": 25,
            "gold_reward": 8,
            "description": "Rattling bones animated by dark magic.",
        },
        "orc": {
            "name": "Orc",
            "hp": 50,
            "attack": 12,
            "defense": 5,
            "xp_reward": 40,
            "gold_reward": 15,
            "description": "A hulking brute with a rusty axe.",
        },
        "spider": {
            "name": "Giant Spider",
            "hp": 25,
            "attack": 9,
            "defense": 3,
            "xp_reward": 20,
            "gold_reward": 3,
            "description": "An eight-legged horror dripping with venom.",
            # TODO: spider should apply poison status effect on hit
        },
        "troll": {
            "name": "Cave Troll",
            "hp": 80,
            "attack": 18,
            "defense": 8,
            "xp_reward": 75,
            "gold_reward": 30,
            "description": "A massive creature that regenerates health each turn.",
            # TODO: implement troll regeneration (heal 5 HP at start of each monster turn)
        },
        "wraith": {
            "name": "Wraith",
            "hp": 40,
            "attack": 15,
            "defense": 10,
            "xp_reward": 60,
            "gold_reward": 20,
            "description": "A ghostly figure that drains your life force.",
        },
    }

    # Maps floor ranges to eligible monster keys
    FLOOR_ENCOUNTERS = {
        (1, 3): ["goblin", "spider"],
        (2, 5): ["goblin", "skeleton", "spider"],
        (4, 7): ["skeleton", "orc", "spider"],
        (6, 10): ["orc", "troll", "wraith"],
    }

    @classmethod
    def create(cls, monster_key: str, floor: int = 1) -> Monster:
        """Create a monster instance with stats scaled to the floor level."""
        template = cls.MONSTER_TEMPLATES.get(monster_key)
        if template is None:
            raise ValueError(f"Unknown monster type: {monster_key!r}")

        scale = 1.0 + (floor - 1) * 0.15
        hp = int(template["hp"] * scale)
        return Monster(
            name=template["name"],
            hp=hp,
            max_hp=hp,
            attack=int(template["attack"] * scale),
            defense=int(template["defense"] * scale),
            xp_reward=int(template["xp_reward"] * scale),
            gold_reward=template["gold_reward"],
            description=template.get("description", ""),
        )

    @classmethod
    def random_for_floor(cls, floor: int) -> Monster:
        """Return a random monster appropriate for the given floor."""
        eligible = []
        for (min_floor, max_floor), keys in cls.FLOOR_ENCOUNTERS.items():
            if min_floor <= floor <= max_floor:
                eligible.extend(keys)

        if not eligible:
            eligible = ["goblin"]

        key = random.choice(eligible)
        return cls.create(key, floor)
