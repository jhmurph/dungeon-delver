"""Player character module."""

from dungeon.config import (
    PLAYER_START_HP,
    PLAYER_START_ATTACK,
    PLAYER_START_DEFENSE,
    PLAYER_LEVEL_UP_BASE_XP,
    MAX_INVENTORY_SIZE,
)


class Player:
    """Represents the player character.

    Attributes:
        name: The player's name.
        hp: Current hit points.
        max_hp: Maximum hit points.
        attack: Attack power.
        defense: Defense rating.
        level: Current level.
        experience: Current XP.
        xp_threshold: XP needed to level up.
        inventory: List of held items.
        gold: Amount of gold carried.
    """

    def __init__(self, name: str):
        self.name = name
        self.hp = PLAYER_START_HP
        self.max_hp = PLAYER_START_HP
        self.attack = PLAYER_START_ATTACK
        self.defense = PLAYER_START_DEFENSE
        self.level = 1
        self.experience = 0
        self.xp_threshold = PLAYER_LEVEL_UP_BASE_XP
        self.inventory = []
        self.gold = 0
        self.kills = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """Apply damage to the player. Returns actual damage taken."""
        actual = max(1, amount)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount: int) -> int:
        """Heal the player. Returns amount actually healed."""
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def add_experience(self, xp: int):
        """Add experience points and trigger level up if threshold is reached."""
        self.experience += xp
        if self.experience >= self.xp_threshold:
            self.level_up()

    def level_up(self):
        """Level up the player, increasing stats."""
        self.level += 1
        self.experience = 0
        self.xp_threshold = int(self.xp_threshold * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 3
        self.defense += 1
        print(f"\n*** LEVEL UP! You are now level {self.level}! ***")
        print(f"    HP: {self.max_hp}  ATK: {self.attack}  DEF: {self.defense}")

    def add_item(self, item) -> bool:
        """Add item to inventory. Returns False if inventory is full."""
        if len(self.inventory) >= MAX_INVENTORY_SIZE - 1:
            print("Your inventory is full!")
            return False
        self.inventory.append(item)
        return True

    def remove_item(self, item) -> bool:
        """Remove item from inventory. Returns False if item not found."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def get_stat(self, stat_name: str):
        """Get a stat value by name."""
        return getattr(self, stat_name, None)

    def get_inventory_display(self) -> str:
        if not self.inventory:
            return "Inventory is empty."
        lines = [f"Inventory ({len(self.inventory)}/{MAX_INVENTORY_SIZE}):"]
        for i, item in enumerate(self.inventory):
            lines.append(f"  {i + 1}. {item.name} - {item.description}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, level={self.level}, hp={self.hp}/{self.max_hp})"
