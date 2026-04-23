"""Game configuration constants."""

# Player settings
PLAYER_START_HP = 100
PLAYER_START_ATTACK = 10
PLAYER_START_DEFENSE = 5
PLAYER_LEVEL_UP_BASE_XP = 100
MAX_INVENTORY_SIZE = 10

# Combat settings
BASE_CRIT_CHANCE = 0.1
CRIT_MULTIPLIER = 2.0
FLEE_SUCCESS_CHANCE = 0.5  # TODO: wire this up when flee is implemented

# Dungeon settings
DUNGEON_DEPTH = 10
ROOMS_PER_FLOOR = 5
MONSTER_SPAWN_CHANCE = 0.7
TREASURE_SPAWN_CHANCE = 0.3  # unused currently

# Item settings
POTION_HEAL_AMOUNT = 30
ELIXIR_HEAL_AMOUNT = 75  # TODO: implement elixir item
POISON_DAMAGE_PER_TURN = 5  # TODO: implement poison status effect

# Display
ROOM_WIDTH = 40
