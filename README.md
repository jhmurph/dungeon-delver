# Dungeon Delver

A text-based dungeon crawler where you descend into a monster-filled dungeon seeking glory and treasure. Fight monsters, collect loot, and see how deep you can go before meeting your end.

## Features

- Turn-based combat system
- Procedurally generated dungeon rooms
- Item and inventory system
- Player progression and leveling
- Multiple monster types with unique traits
- Gold economy

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python -m dungeon.main
```

Or if installed:

```bash
dungeon-delver
```

## Gameplay

Navigate through dungeon rooms using the command prompt. Available commands:

| Command | Description |
|---------|-------------|
| `move <direction>` | Move north/south/east/west |
| `attack` | Attack the monster in the current room |
| `flee` | Attempt to escape combat |
| `use <number>` | Use item #N from your inventory |
| `take` | Pick up items in the current room |
| `inventory` | Show current inventory and gold |
| `stats` | Show player statistics |
| `look` | Re-describe the current room |
| `descend` | Go down the stairs (if present) |
| `map` | Display dungeon map |
| `help` | Show command reference |
| `quit` | Quit the game |

Direction shortcuts: `n`, `s`, `e`, `w`

## Controls

[TODO: Add full controls reference including keyboard shortcuts]

## Save / Load

Game progress can be saved and loaded from disk... [TODO: document save system once implemented]

## Project Structure

```
dungeon-delver/
├── src/
│   └── dungeon/
│       ├── config.py     # Game constants and tuning values
│       ├── player.py     # Player character class
│       ├── monster.py    # Monster definitions and factory
│       ├── items.py      # Item classes and factory
│       ├── combat.py     # Combat resolution system
│       ├── dungeon.py    # Room and dungeon generation
│       ├── game.py       # Main game loop and command handling
│       └── utils.py      # Shared utility functions
└── tests/
    ├── test_player.py
    ├── test_combat.py
    └── test_items.py
```

## Contributing

Run the test suite with:

```bash
pytest
```
