"""Main game loop and command handling."""

import random
from dungeon.player import Player
from dungeon.dungeon import Dungeon
from dungeon.combat import Combat, CombatResult
from dungeon.items import create_item, HealingPotion


HELP_TEXT = """
Commands:
  move <direction>   Move north / south / east / west  (shortcuts: n s e w)
  attack             Attack the monster in this room
  flee               Attempt to escape from combat
  use <number>       Use item #N from your inventory
  take               Pick up all items in the current room
  inventory / inv    Show inventory and gold
  stats              Show player statistics
  look               Re-describe the current room
  descend            Go down the stairs (if present)
  map                Show dungeon map
  save               Save the game
  help               Show this message
  quit               Quit the game
"""


class Game:
    """Manages overall game state and the main command loop."""

    def __init__(self):
        self.player: Player = None
        self.dungeon: Dungeon = None
        self.running = False
        self.current_combat: Combat = None

    def start(self):
        """Initialize a new game and begin the main loop."""
        print("=" * 50)
        print("    DUNGEON DELVER — Enter at Your Own Risk")
        print("=" * 50)

        name = input("\nEnter your hero's name: ").strip()
        if not name:
            name = "Adventurer"

        self.player = Player(name)
        self.dungeon = Dungeon()

        starting_potion = create_item("minor_potion")
        self.player.add_item(starting_potion)

        print(f"\nWelcome, {self.player.name}! You stand at the dungeon entrance.")
        print("Type 'help' for a list of commands.\n")

        first_room = self.dungeon.current_room()
        first_room.visited = True
        print(first_room.describe())

        self.running = True
        self._game_loop()

    def _game_loop(self):
        """Main input loop. Runs until the player dies or quits."""
        while self.running and self.player.is_alive():
            try:
                raw = input("\n> ").strip().lower()
                if not raw:
                    continue
                parts = raw.split()
                cmd = parts[0]
                args = parts[1:]
                self._handle_command(cmd, args)
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
            # No general exception handler — unexpected errors will surface as tracebacks

        if not self.player.is_alive():
            self._game_over()

    def _handle_command(self, cmd: str, args: list):
        aliases = {
            "inv": "inventory",
            "i": "inventory",
            "n": "move north",
            "s": "move south",
            "e": "move east",
            "w": "move west",
        }
        if cmd in aliases:
            parts = aliases[cmd].split()
            cmd = parts[0]
            if len(parts) > 1:
                args = parts[1:]

        handlers = {
            "move": self._cmd_move,
            "attack": self._cmd_attack,
            "flee": self._cmd_flee,
            "use": self._cmd_use,
            "take": self._cmd_take,
            "inventory": self._cmd_inventory,
            "stats": self._cmd_stats,
            "look": self._cmd_look,
            "descend": self._cmd_descend,
            "map": self._cmd_map,
            "save": self._cmd_save,
            "help": self._cmd_help,
            "quit": self._cmd_quit,
        }

        handler = handlers.get(cmd)
        if handler:
            handler(args)
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for commands.")

    # ------------------------------------------------------------------ commands

    def _cmd_move(self, args):
        if not args:
            print("Move where? (north / south / east / west)")
            return

        room = self.dungeon.current_room()
        if room.monster and room.monster.is_alive():
            print(f"You can't leave — the {room.monster.name} blocks the way!")
            return

        direction = args[0]
        new_room = self.dungeon.move(direction)
        if new_room is None:
            print(f"You can't go {direction} from here.")
        else:
            print(new_room.describe())
            if new_room.monster and new_room.monster.is_alive():
                print(f"\nA {new_room.monster.name} lunges toward you!")

    def _cmd_attack(self, args):
        room = self.dungeon.current_room()
        if not room.monster or not room.monster.is_alive():
            print("There's nothing to attack here.")
            return

        if self.current_combat is None or self.current_combat.monster is not room.monster:
            self.current_combat = Combat(self.player, room.monster)

        p_msg, m_msg = self.current_combat.do_turn()
        print(p_msg)
        if m_msg:
            print(m_msg)

        status = self.current_combat.get_status()
        if status == CombatResult.PLAYER_WIN:
            self.current_combat.award_victory()
            self.current_combat = None
            if random.random() < 0.3:
                drop = create_item("minor_potion")
                room.items.append(drop)
                print(f"The {room.monster.name} dropped a {drop.name}!")
        elif status == CombatResult.PLAYER_DEAD:
            pass  # _game_loop handles this after returning

    def _cmd_flee(self, args):
        if self.current_combat is None:
            print("You're not in combat.")
            return
        self.current_combat.flee()

    def _cmd_use(self, args):
        if not args:
            print("Use which item? Specify a number (e.g., 'use 1').")
            return
        try:
            idx = int(args[0]) - 1
        except ValueError:
            print("Please specify an item number (e.g., 'use 1').")
            return

        if idx < 0 or idx >= len(self.player.inventory):
            print("Invalid item number.")
            return

        item = self.player.inventory[idx]
        msg = item.use(self.player)
        print(msg)

        if isinstance(item, HealingPotion):
            self.player.remove_item(item)

    def _cmd_take(self, args):
        room = self.dungeon.current_room()
        if not room.items:
            print("There's nothing on the ground here.")
            return
        for item in list(room.items):
            if self.player.add_item(item):
                room.items.remove(item)
                print(f"You pick up the {item.name}.")

    def _cmd_inventory(self, args):
        print(self.player.get_inventory_display())
        print(f"Gold: {self.player.gold}")

    def _cmd_stats(self, args):
        p = self.player
        print(f"\n--- {p.name} ---")
        print(f"Level : {p.level}")
        print(f"HP    : {p.hp}/{p.max_hp}")
        print(f"ATK   : {p.attack}")
        print(f"DEF   : {p.defense}")
        print(f"XP    : {p.experience}/{p.xp_threshold}")
        print(f"Gold  : {p.gold}")
        print(f"Kills : {p.kills}")
        print(f"Floor : {self.dungeon.floor}")

    def _cmd_look(self, args):
        print(self.dungeon.current_room().describe())

    def _cmd_descend(self, args):
        room = self.dungeon.current_room()
        if room.monster and room.monster.is_alive():
            print("Defeat the monster before descending!")
            return
        self.dungeon.descend()
        print(self.dungeon.current_room().describe())

    def _cmd_map(self, args):
        self.dungeon.display_map()

    def _cmd_save(self, args):
        # TODO: implement save/load using JSON serialization of game state
        print("Save/load is not yet implemented.")

    def _cmd_help(self, args):
        print(HELP_TEXT)

    def _cmd_quit(self, args):
        print("Thanks for playing Dungeon Delver. Until next time!")
        self.running = False

    # ------------------------------------------------------------------ end state

    def _game_over(self):
        p = self.player
        print("\n" + "=" * 50)
        print("    YOU HAVE DIED")
        print("=" * 50)
        print(f"\n{p.name} fell in the dungeon on floor {self.dungeon.floor}.")
        print(f"Monsters slain: {p.kills}  |  Gold collected: {p.gold}")
        print("\nBetter luck next time, adventurer.")
