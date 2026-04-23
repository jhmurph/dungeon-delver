"""Dungeon map and room generation."""

import random
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from dungeon.config import MONSTER_SPAWN_CHANCE, ROOMS_PER_FLOOR
from dungeon.monster import MonsterFactory, Monster


DIRECTIONS = ["north", "south", "east", "west"]
OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}


@dataclass
class Room:
    """A single room in the dungeon."""

    room_id: int
    floor: int
    name: str
    description: str
    exits: Dict[str, int] = field(default_factory=dict)  # direction -> room_id
    monster: Optional[Monster] = None
    items: List = field(default_factory=list)
    visited: bool = False
    is_stairs_down: bool = False

    def describe(self) -> str:
        lines = [f"\n=== {self.name} (Floor {self.floor}) ===", self.description]

        if self.monster and self.monster.is_alive():
            lines.append(f"\nA {self.monster.name} lurks here! [{self.monster.getStatus()}]")

        if self.items:
            names = ", ".join(i.name for i in self.items)
            lines.append(f"Items on the ground: {names}")

        if self.exits:
            dirs = ", ".join(sorted(self.exits.keys()))
            lines.append(f"Exits: {dirs}")

        if self.is_stairs_down:
            lines.append("A stone staircase descends into darkness.")

        return "\n".join(lines)


class Dungeon:
    """Manages dungeon floors and room navigation.

    Rooms are generated procedurally per floor. Each floor has ROOMS_PER_FLOOR
    rooms linked in a chain, with one staircase at the far end.
    """

    def __init__(self):
        self.floor = 1
        self.rooms: Dict[int, Room] = {}
        self.current_room_id: int = 0
        self._next_room_id = 0
        self.generate_floor(self.floor)

    def _get_id(self) -> int:
        rid = self._next_room_id
        self._next_room_id += 1
        return rid

    def _generateRoomName(self, floor: int) -> str:  # inconsistency: camelCase vs rest of module
        prefixes = ["Damp", "Dark", "Narrow", "Crumbling", "Forgotten", "Ancient", "Mossy"]
        suffixes = ["Corridor", "Chamber", "Hall", "Alcove", "Vault", "Passage", "Antechamber"]
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"

    def _generate_description(self, floor: int) -> str:
        descriptions = [
            "Torch sconces line the walls, casting flickering shadows.",
            "Water drips from the ceiling, pooling on the uneven stone floor.",
            "Bones crunch underfoot. Something died here not long ago.",
            "A foul smell hangs in the air. You feel uneasy.",
            "Strange glowing runes cover every surface.",
            "Cobwebs fill every corner. This place hasn't been disturbed in ages.",
            "The floor is slick with moisture. You tread carefully.",
            "A cold wind rushes through from somewhere unseen.",
            # TODO: add more varied descriptions for deeper floors
        ]
        return random.choice(descriptions)

    def generate_floor(self, floor: int):
        """Generate all rooms for a dungeon floor and reset navigation."""
        self.rooms.clear()

        start_id = self._get_id()
        start_room = Room(
            room_id=start_id,
            floor=floor,
            name="Entry Chamber",
            description="You descend into this musty chamber. Dust motes float in the dim light.",
        )
        self.rooms[start_id] = start_room
        self.current_room_id = start_id

        prev_id = start_id
        room_ids = [start_id]

        for _ in range(ROOMS_PER_FLOOR - 1):
            new_id = self._get_id()
            name = self._generateRoomName(floor)
            desc = self._generate_description(floor)

            has_monster = random.random() < MONSTER_SPAWN_CHANCE
            monster = MonsterFactory.random_for_floor(floor) if has_monster else None

            room = Room(
                room_id=new_id,
                floor=floor,
                name=name,
                description=desc,
                monster=monster,
            )
            self.rooms[new_id] = room
            room_ids.append(new_id)

            dir_forward = random.choice(["north", "east"])
            dir_back = OPPOSITE[dir_forward]
            self.rooms[prev_id].exits[dir_forward] = new_id
            room.exits[dir_back] = prev_id
            prev_id = new_id

        self.rooms[room_ids[-1]].is_stairs_down = True

    def current_room(self) -> Room:
        return self.rooms[self.current_room_id]

    def move(self, direction: str) -> Optional[Room]:
        """Move the player in the given direction. Returns the new room or None if blocked."""
        room = self.current_room()
        if direction not in room.exits:
            return None
        self.current_room_id = room.exits[direction]
        new_room = self.current_room()
        new_room.visited = True
        return new_room

    def descend(self) -> bool:
        """Descend to the next floor via the staircase. Returns False if not at stairs."""
        if not self.current_room().is_stairs_down:
            print("There are no stairs here.")
            return False
        self.floor += 1
        self.generate_floor(self.floor)
        print(f"\nYou descend to floor {self.floor}...")
        return True

    def display_map(self):
        """Display a simple map of visited rooms on this floor."""
        # TODO: implement ASCII map display showing room connectivity
        visited = [r for r in self.rooms.values() if r.visited]
        print(f"[Floor {self.floor} — {len(visited)}/{len(self.rooms)} rooms explored]")
        print("[Full map display not yet available]")
