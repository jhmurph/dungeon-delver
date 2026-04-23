"""Item definitions for the dungeon."""

from typing import Optional
from dungeon.config import POTION_HEAL_AMOUNT, ELIXIR_HEAL_AMOUNT


class Item:
    """Base class for all items."""

    def __init__(self, name: str, description: str, value: int = 0):
        self.name = name
        self.description = description
        self.value = value  # gold value for selling

    def use(self, player) -> str:
        """Use this item on the player. Returns a message describing the effect."""
        return f"You use the {self.name} but nothing happens."

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"


class HealingPotion(Item):
    """A potion that restores hit points."""

    def __init__(self, strength: str = "minor"):
        if strength == "minor":
            heal_amount = POTION_HEAL_AMOUNT
            name = "Minor Healing Potion"
            desc = f"Restores {POTION_HEAL_AMOUNT} HP."
        elif strength == "major":
            heal_amount = ELIXIR_HEAL_AMOUNT
            name = "Major Healing Potion"
            desc = f"Restores {ELIXIR_HEAL_AMOUNT} HP."
        else:
            heal_amount = POTION_HEAL_AMOUNT
            name = "Healing Potion"
            desc = f"Restores {POTION_HEAL_AMOUNT} HP."

        super().__init__(name=name, description=desc, value=10)
        self.heal_amount = heal_amount

    def use(self, player) -> str:
        healed = player.heal(self.heal_amount)
        return f"You drink the {self.name} and restore {healed} HP."


class Weapon(Item):
    """A weapon that increases attack power when equipped."""

    def __init__(self, name: str, attack_bonus: int, description: str = "", value: int = 20):
        super().__init__(
            name=name,
            description=description or f"+{attack_bonus} attack.",
            value=value,
        )
        self.attack_bonus = attack_bonus
        self.equipped = False

    def use(self, player) -> str:
        # TODO: implement proper equipment slots so bonuses aren't stackable
        # Currently applying the bonus directly; calling use() twice stacks the bonus
        player.attack += self.attack_bonus
        self.equipped = True
        return f"You equip the {self.name}. Attack +{self.attack_bonus}."


class Armor(Item):
    """Armor that increases defense when equipped."""

    def __init__(self, name: str, defense_bonus: int, description: str = "", value: int = 25):
        super().__init__(
            name=name,
            description=description or f"+{defense_bonus} defense.",
            value=value,
        )
        self.defense_bonus = defense_bonus
        self.equipped = False

    def use(self, player) -> str:
        # TODO: implement proper equipment slots
        player.defense += self.defense_bonus
        self.equipped = True
        return f"You equip the {self.name}. Defense +{self.defense_bonus}."


class PoisonPotion(Item):
    """A vial of poison that can be thrown at enemies during combat."""

    def __init__(self):
        super().__init__(
            name="Poison Vial",
            description="A vial of murky liquid. Throw at an enemy during combat.",
            value=15,
        )

    def use(self, player) -> str:
        # TODO: implement throwing items at enemies during combat
        return "You'd need to throw this at an enemy. Use it during combat."


class KeyItem(Item):
    """A special key that opens locked doors."""

    def __init__(self, key_id: str):
        super().__init__(
            name=f"Iron Key ({key_id})",
            description="A heavy iron key. There must be a door it fits.",
            value=0,
        )
        self.key_id = key_id

    def use(self, player) -> str:
        return "You hold up the key. Find a locked door to use it on."


# Item spawn tables used by the dungeon generator
COMMON_ITEMS = ["minor_potion"]
UNCOMMON_ITEMS = ["major_potion", "short_sword", "leather_armor"]
RARE_ITEMS = ["long_sword", "chain_mail", "poison_vial"]


def create_item(item_key: str) -> Optional[Item]:
    """Factory function — creates an item instance by key string."""
    registry = {
        "minor_potion": lambda: HealingPotion("minor"),
        "major_potion": lambda: HealingPotion("major"),
        "short_sword": lambda: Weapon("Short Sword", attack_bonus=4, value=15),
        "long_sword": lambda: Weapon("Long Sword", attack_bonus=8, value=35),
        "leather_armor": lambda: Armor("Leather Armor", defense_bonus=3, value=20),
        "chain_mail": lambda: Armor("Chain Mail", defense_bonus=6, value=50),
        "poison_vial": lambda: PoisonPotion(),
    }
    factory = registry.get(item_key)
    return factory() if factory else None
